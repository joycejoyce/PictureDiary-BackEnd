from datetime import date
from os import mkdir, path

def get(message):
    currentDateStr = getCurrentDateStr()
    fileName = getFileName(message, currentDateStr)
    fileExtension = getFileExtension(message)
    fullFileName = "%s.%s" % (fileName , fileExtension)

    folderPath = getFolderPath(currentDateStr)

    filePath = getFilePath(folderPath, fullFileName)

    return filePath

def getCurrentDateStr():
    today = date.today().strftime("%Y%m%d")
    return today

def getFileName(msg, currentDateStr):
    fileName = "LINE_%s_%s" % (currentDateStr, msg.id)
    # print("fileName: " + fileName)
    return fileName

def getFileExtension(message):
    msgType = message.type

    fileExtension = ""
    if msgType == "text":
        fileExtension = "txt"
    elif msgType == "image":
        fileExtension = "jpg"
    elif msgType == "video":
        fileExtension = "mp4"
    else:
        raise Exception("Unexpected msgType: [%s]" % msgType)

    return fileExtension

def getFolderPath(currentDateStr):
    try:
        folderPath = currentDateStr
        if not path.exists(folderPath):
            mkdir(folderPath)
        return folderPath
    except OSError:
        print ("Create folder [%s] failed" % folderPath)

def getFilePath(folderPath, fullFileName):
    filePath = folderPath + "/" + fullFileName
    print("filePath: [%s]" % filePath)
    return filePath