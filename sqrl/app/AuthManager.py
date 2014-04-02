from datetime import datetime
from uuid import uuid4
from django.utils.timezone import utc
from django.contrib.auth import authenticate
from models import PendingAuth, PendingLogin, SQRLUser
from QRFileManager import createQRImage, deleteImage
from sqrl import settings
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode


def extractTokenFromUrl(url):
    substrings = url.split("/")
    return substrings[len(substrings)-1]

def expired(dateTime, timeout):
    timeElapsed = datetime.utcnow().replace(tzinfo=utc) - dateTime
    return (timeElapsed.seconds / 60) > timeout

def verifySignature(key_text, signature, data):
    key = RSA.importKey(key_text)
    signer = PKCS1_v1_5.new(key)
    datahash = SHA256.new(data)
    return signer.verify(datahash, signature)

def sqrlAuthenticate(token, key, signature):
    print "Authenticating with token %s" % token
    success = False
    returnUrl = ""
    try:
        user = SQRLUser.objects.get(identity_key=key)
        pendingAuth = PendingAuth.objects.get(token=token)
        data = pendingAuth.url
        if expired(pendingAuth.datetime, settings.PENDING_AUTH_TIMEOUT):
            print "Expired auth token."
        elif not verifySignature(b64decode(key), b64decode(signature), data):
            print "Invalid signature."
        else:
            success = True
            createNewLogin(token, user.get_username())
    except SQRLUser.DoesNotExist:
        print "Invalid identity key."
    except PendingAuth.DoesNotExist:
        print "Invalid auth token."

    return success

def loginAuthenticate(token):
    print "Logging in with token %s" % token
    user = None
    try:
        pendingLogin = PendingLogin.objects.get(token=token)
        if expired(pendingLogin.datetime, settings.PENDING_AUTH_TIMEOUT):
            print "Expired login token."
            return None
        user = authenticate(username=pendingLogin.username, password=settings.SHARED_USER_PASSWORD)
        if user is None:
            print "Invalid username."
    except PendingLogin.DoesNotExist:
        print "Invalid login token."

    return user

def createToken():
    return uuid4().hex

def createNewAuth():
    token = createToken()
    url = settings.AUTHENTICATION_URL_FORMAT_STRING % token
    filename = createQRImage(token, settings.QRCODE_PATH, url)
    PendingAuth.objects.create(token=token, url=url)
    return filename, token

def createNewLogin(token, username):
    PendingLogin.objects.create(token=token, username=username)

def cleanUpPendingSessions():
    for s in PendingAuth.objects.all():
        deleteImage(s.id, settings.QRCODE_PATH)
    PendingAuth.objects.all().delete()
    PendingLogin.objects.all().delete()
