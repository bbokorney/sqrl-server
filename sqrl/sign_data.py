from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode
from sys import argv

def sign_data(key_text, data):
    key = RSA.importKey(key_text)
    signer = PKCS1_v1_5.new(key)
    hash = SHA256.new(data)
    sign = signer.sign(hash)
    return b64encode(sign)

script, key_file_loc, data_file_loc = argv

key_text = open(key_file_loc, "r").read()
data = open(data_file_loc, "r").read()
print sign_data(key_text, data)



