from GoogleDriveProcessor import getService, getInfoAry_filesInFolder
from GlobalVar import MimeType, LineContentFolderId
import json

service = None

def get(dayNum, lastDate):
    global service
    service = getService()

    allFolderNames = getAllDateFolderNames()

    # sortedFolderNames = sorted(allDateFolderNames, reverse = True)

    # targetFolderNames = getTargetFolderNames(sortedFolderNames)

    # jsonAry = getJsonAry(targetFolderNames)

    # return jsonAry
    return []

def getAllDateFolderNames():
    mimeType = MimeType.get("Folder")
    parentFolderId = LineContentFolderId
    fieldName_id = "id"
    fieldName_name = "name"
    includeFoldersOfNoSubFolder = False

    infoAry = getInfoAry_filesInFolder(mimeType, parentFolderId, fieldName_id, fieldName_name, includeFoldersOfNoSubFolder)
    
    print("infoAry", json.dumps(infoAry))

    return infoAry