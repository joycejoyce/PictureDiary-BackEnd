from datetime import date
from os import mkdir, listdir, path
from os.path import isfile, join
import re

def get(fileExtension):
    currentDateStr = getCurrentDateStr()
    folderPath = getFolderPath(currentDateStr)
    maxFileNo = getMaxFileNo(folderPath, currentDateStr)
    filePath = getFilePath(folderPath, currentDateStr, maxFileNo, fileExtension)
    return filePath

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
    allfilePaths = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and isfilePathMatched(currentDateStr, f)]
    for f in allfilePaths:
        print ("matched filePath:" + f)

    allNo = getAllNo(allfilePaths)
    if len(allNo) > 0:
        maxNo = int(allNo[-1])
    else:
        maxNo = 0

    return maxNo

def isfilePathMatched(prefix, filePath):
    pattern = re.compile(prefix + "_.+")
    isMatched = pattern.match(filePath)
    if isMatched:
        print ("'%s' matched" % filePath)
        return True
    else:
        print ("'%s' not matched" % filePath)
        return False

def getAllNo(allfilePaths):
    nums = []
    for f in allfilePaths:
        matchObj = re.search(r"_\d{2}\.", f)
        if matchObj:
            startPos = matchObj.span()[0] + 1
            endPos = matchObj.span()[1] - 1
            num = f[startPos : endPos]
            nums.append(num)
    nums = sorted(nums)
    return nums

def getFilePath(folderPath, currentDateStr, maxFileNo, fileExtension):
    paddingZero = format(maxFileNo+1, '02')
    return folderPath + "/" + currentDateStr + "_" + paddingZero + "." + fileExtension