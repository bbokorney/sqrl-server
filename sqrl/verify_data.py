from sys import argv
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode

def verify_signature(pubkey_text, signature, data):
    pubkey = RSA.importKey(pubkey_text)
    signer = PKCS1_v1_5.new(pubkey)
    hash = SHA256.new(data)
    return signer.verify(hash, b64decode(signature))


script, key_file_loc, signature_file_loc, data_file_loc = argv

pubkey_text = open(key_file_loc, "r").read()
signature = open(signature_file_loc, "r").read()
data = open(data_file_loc, "r").read()
print verify_signature(pubkey_text, signature, data)