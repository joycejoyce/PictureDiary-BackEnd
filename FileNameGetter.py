from datetime import date
from os import mkdir, listdir, path
from os.path import isfile, join
import re

def get():
    print("Enter get()")
    currentDateStr = getCurrentDateStr()
    folderPath = getFolderPath()
    maxFileNo = getMaxFileNo(folderPath, currentDateStr)
    return "a"

def getCurrentDateStr():
    today = date.today().strftime("%Y%m%d")
    print("today:", today)
    return today

def getFolderPath():
    try:
        folderPath = "tmp"
        if not path.exists(folderPath):
            mkdir(folderPath)
        return folderPath
    except OSError:
        print ("Creation of the directory '%s' failed" % folderPath)

def getMaxFileNo(folderPath, currentDateStr):
    allFileNames = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and isFileNameMatched(currentDateStr, f)]
    for f in allFileNames:
        print ("matched fileName:" + f)
    return 2

def isFileNameMatched(prefix, fileName):
    pattern = re.compile(prefix + "_.+")
    isMatched = pattern.match(fileName)
    if isMatched:
        print ("'%s' matched" % fileName)
        return True
    else:
        print ("'%s' not matched" % fileName)
        return False