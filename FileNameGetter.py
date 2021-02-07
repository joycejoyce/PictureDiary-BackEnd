from datetime import date
from os import mkdir, listdir, path
from os.path import isfile, join
import re

def get(fileExtension):
    currentDateStr = getCurrentDateStr()
    folderPath = getFolderPath(currentDateStr)
    maxFileNo = getMaxFileNo(folderPath, currentDateStr)
    fileName = getFileName(folderPath, currentDateStr, maxFileNo, fileExtension)
    return fileName

def getCurrentDateStr():
    today = date.today().strftime("%Y%m%d")
    return today

def getFolderPath(currentDateStr):
    try:
        folderPath = currentDateStr
        if not path.exists(folderPath):
            mkdir(folderPath)
        return folderPath
    except OSError:
        print ("Creation of the directory '%s' failed" % folderPath)

def getMaxFileNo(folderPath, currentDateStr):
    allFileNames = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and isFileNameMatched(currentDateStr, f)]
    for f in allFileNames:
        print ("matched fileName:" + f)

    allNo = getAllNo(allFileNames)
    if len(allNo) > 0:
        maxNo = int(allNo[-1])
    else:
        maxNo = 0

    return maxNo

def isFileNameMatched(prefix, fileName):
    pattern = re.compile(prefix + "_.+")
    isMatched = pattern.match(fileName)
    if isMatched:
        print ("'%s' matched" % fileName)
        return True
    else:
        print ("'%s' not matched" % fileName)
        return False

def getAllNo(allFileNames):
    nums = []
    for f in allFileNames:
        matchObj = re.search(r"_\d{2}\.", f)
        if matchObj:
            startPos = matchObj.span()[0] + 1
            endPos = matchObj.span()[1] - 1
            num = f[startPos : endPos]
            nums.append(num)
    nums = sorted(nums)
    return nums

def getFileName(folderPath, currentDateStr, maxFileNo, fileExtension):
    paddingZero = format(maxFileNo, '02')
    return folderPath + "/" + currentDateStr + "_" + paddingZero + "." + fileExtension