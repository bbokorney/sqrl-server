import os

EXECUTABLE_NAME = "qrcode.exe"
FILE_SUFFIX = ".png"
SIZE = 10

def addFilenameSuffix(filename):
    return "%s%s" % (filename, FILE_SUFFIX)

def createQRImage(id, prefix, data):
    filename = addFilenameSuffix(id)
    cmd = EXECUTABLE_NAME + " -o \"%s\" -s %s \"%s\"" % (os.path.join(prefix, filename), SIZE, data)
    print cmd
    os.system(cmd)
    return filename

def deleteImage(id, prefix):
    absPath = os.path.join(prefix, addFilenameSuffix(id))
    if os.path.isfile(absPath):
        os.remove(absPath)