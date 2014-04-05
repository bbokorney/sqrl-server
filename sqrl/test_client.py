from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode
from sys import argv
import requests
import codecs


def getPublicKey(key_text):
    key = RSA.importKey(key_text)
    return key.publickey().exportKey()

def signData(key_text, data):
    key = RSA.importKey(key_text)
    signer = PKCS1_v1_5.new(key)
    hasher = SHA256.new(data)
    sign = signer.sign(hasher)
    return sign

def sendPost(url, data):
    response = requests.post(url, data)
    print response.cookies
    print response.headers
    print response.text

def auth(url, key_file_loc):
    key_text = codecs.open(key_file_loc, "r", "ascii").read()
    sig = signData(key_text, url)
    pub_key_text = getPublicKey(key_text)
    params = {"idk": b64encode(pub_key_text), "sig": b64encode(sig)}
    print sendPost(url, params)


if len(argv) != 3:
    print "Invalid parameters. Proper usage:"
    print "url key_file"
    exit()


auth(argv[1], argv[2])
