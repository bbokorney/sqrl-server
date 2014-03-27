from datetime import datetime
from django.utils.timezone import utc
from models import UnclaimedSession
from QRFileManager import createQRImage, deleteImage
from sqrl import settings

def authenticate():
    return True

def getNewSession():
    newSession = UnclaimedSession.objects.create()
    filename = newSession.id
    filename = createQRImage(newSession.id, settings.QRCODE_PATH, "http://%s/app/login/%s" % (settings.HOSTNAME, filename))
    return filename

def claimSession(id):
    success = False
    try:
        sessionId = UnclaimedSession.objects.get(id=id)
        timeElapsed = datetime.utcnow().replace(tzinfo=utc) - sessionId.datetime
        sessionId.delete()
        deleteImage(id, settings.QRCODE_PATH)
        if (timeElapsed.seconds / 60) < settings.UNCLAIMED_SESSION_TIMEOUT:
            print "They're okay!"
            success = True
        else:
            print "Too slow"
    except UnclaimedSession.DoesNotExist:
        print "That id's not even in the db!"
        success = False
    return success