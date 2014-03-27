from os import system

EXECUTABLE_NAME = "qrcode.exe"

def createQRImage(filename, data):
    cmd = EXECUTABLE_NAME + " -o %s.png -s 15 \"%s\"" % (filename, data)
    print cmd
    system(cmd)
