import os

def getFolderName(filePath):
    return os.path.dirname(filePath)

def getFileName(filePath):
    return os.path.basename(filePath)

def getFileExtension(filePath):
    fileName, ext = os.path.splitext(filePath)
    ext = ext[1:]
    return ext