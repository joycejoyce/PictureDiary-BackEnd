from GoogleDriveProcessor import getService, getInfoAry_filesInFolder, getFileContent
from GlobalVar import AllJsonFileName, MimeType, LineContentFolderId
import json

def get():
    mimeType = MimeType.get("Text")
    parentFolderId = LineContentFolderId
    fieldName_id = "id"
    fieldName_name = "name"
    includeFoldersOfNoSubFolder = False

    infoAry = getInfoAry_filesInFolder(mimeType, parentFolderId, fieldName_id, fieldName_name, includeFoldersOfNoSubFolder)
    print("infoAry", infoAry)

    resultJson = json.loads("[]")

    if len(infoAry) != 0:
        binaryContent = getFileContent(infoAry[0].get(fieldName_id))
        text = binaryContent.decode("utf-8")
        print("text", text)
        resultJson = json.loads(text)
    
    return json.dumps(resultJson)
