import json
import chardet
import codecs
import ntpath
import os
import io
from GoogleDriveProcessor import getService, getInfoAry_filesInFolder
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from GlobalVar import LineContentFolderId, AllJsonFileName

service = None
isTest = False
MimeType = {
    "Folder": "application/vnd.google-apps.folder",
    "Text": "text/plain",
    "Img": "image/jpeg"
}
JsonFieldNames = [
    "dateId",
    "date",
    "id",
    "title",
    "text"
]
outputFileName = AllJsonFileName

def gen():
    global service
    service = getService()

    rootFolderId = getRootFolderId()

    infoAry_dateFolder = getInfoAry_dateFolder(rootFolderId) # JSON array of: id_dateFolder / date
    print("infoAry_dateFolder", json.dumps(infoAry_dateFolder))

    infoAry_titleFolder = getInfoAry_titleFolder(infoAry_dateFolder) # JSON array of: id / title / text / imgUrls
    print("infoAry_titleFolder", json.dumps(infoAry_titleFolder))

    writeJsonToFile(infoAry_titleFolder, outputFileName)

    deleteDriveFile_byFilename(outputFileName, rootFolderId)

    uploadFileToFolder(outputFileName, MimeType.get("Text"), rootFolderId)

    deleteLocalFile(outputFileName)

def getRootFolderId():
    return LineContentFolderId

def getInfoAry_dateFolder(parentFolderId):
    global isTest
    if isTest:
        return [
            {
                "id_dateFolder": "1lUqAm91OzLYt4ZgERsscfZmjE9VkOJxx",
                "date": "20210404"
            }
        ]

    includeFoldersOfNoSubFolder = True
    infoAry_dateFolder = getInfoAry_filesInFolder(MimeType.get("Folder"), parentFolderId, "id_dateFolder", "date", includeFoldersOfNoSubFolder)
    
    return infoAry_dateFolder

def getInfoAry_titleFolder(infoAry_dateFolder):
    resultJson = json.loads("[]")

    for dateInfo in infoAry_dateFolder:
        dateId = dateInfo.get("id_dateFolder")
        includeFoldersOfNoSubFolder = False
        infoAry_titleFolder = getInfoAry_filesInFolder(MimeType.get("Folder"), dateId, "id", "title", includeFoldersOfNoSubFolder)
        print("infoAry_titleFolder(id & title only)", infoAry_titleFolder)

        if len(infoAry_titleFolder) == 0:
            # resultJson.append(dateInfo)
            continue

        for info_titleFolder in infoAry_titleFolder:
            id_titleFolder = info_titleFolder.get("id")

            obj = {}
            
            date = dateInfo.get("date")
            obj["date"] = date

            title = info_titleFolder.get("title")
            obj["title"] = title

            text = getText(id_titleFolder)
            if text is not None:
                obj["text"] = text
            else:
                obj["text"] = ""

            imgUrls = getImgUrls(id_titleFolder)
            if imgUrls is not None:
                obj["imgUrls"] = imgUrls
            else:
                obj["imgUrls"] = []

            resultJson.append(obj)

    return resultJson

def getText(parentFolderId):
    info_textFile = getInfo_textFile(parentFolderId) # id / content
    # print("info_textFile", info_textFile)

    if info_textFile is None:
        return None

    fileId = info_textFile.get("id")
    binaryContent = info_textFile.get("content")

    encoding = getEncoding(binaryContent)
    print("encoding", encoding)
    
    if encoding.lower() != "utf-8":
        newFileId = createUtf8File(fileId, parentFolderId)
        binaryContent = getFileContent(newFileId)

    text = binaryContent.decode("utf-8")
    print("text", text)

    return text

def getInfo_textFile(folderId):
    fieldName_id = "id"
    fieldName_name = "name"
    includeFoldersOfNoSubFolder = False

    infoAry_filesInFolder = getInfoAry_filesInFolder(
        MimeType.get("Text"),
        folderId,
        fieldName_id,
        fieldName_name,
        includeFoldersOfNoSubFolder
    )
    print("infoAry_filesInFolder: ", infoAry_filesInFolder)

    if len(infoAry_filesInFolder) == 0:
        return None
    else:
        id = infoAry_filesInFolder[0].get(fieldName_id)
        content = getFileContent(id)
        
        obj = {
            "id": id,
            "content": content
        }

        return obj

def getFileContent(fileId):
    return service.files().get_media(fileId = fileId).execute()

def getEncoding(binary):
    return chardet.detect(binary)["encoding"]

def createUtf8File(fileId, parentFolderId):
    fileName = "Text_Of_" + fileId + ".txt"

    downloadFile(fileId, fileName)

    newFileName = getNewFileName(fileName)
    print("newFileName", newFileName)
    with codecs.open(fileName, "r") as origFile:
        origFileContent = origFile.read()
    with codecs.open(newFileName, "w", "utf-8") as newFile:
        newFile.write(origFileContent)

    newFileId = uploadFileToFolder(newFileName, MimeType.get("Text"), parentFolderId)
    print("newFileId", newFileId)

    deleteLocalFile(fileName)
    deleteLocalFile(newFileName)
    deleteDriveFile(fileId)

    return newFileId

def downloadFile(fileId, fileName):
    request = service.files().get_media(fileId = fileId)

    fh = io.FileIO(fileName, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

def getNewFileName(origFileName):
    fileNameWithoutExt = os.path.splitext(origFileName)[0]
    return fileNameWithoutExt

def uploadFileToFolder(filePath, mimeType, parentFolderId):
    fileName = ntpath.basename(filePath)

    media = MediaFileUpload(fileName,
                            mimetype = mimeType,
                            resumable = True)

    fileMetaData = {
        "name": fileName,
        "mimeType": mimeType,
        "parents": [parentFolderId]
    }    

    file = service.files().create(body = fileMetaData, media_body = media, fields = "id").execute()

    fileId = file.get("id")

    return fileId

def deleteLocalFile(filePath):
    os.remove(filePath)

def deleteDriveFile_byFilename(filename, parentFolderId):
    mimeType = MimeType.get("Text")
    fieldName_id = "id"
    fieldName_name = "name"
    includeFoldersOfNoSubFolder = False

    files = getInfoAry_filesInFolder(mimeType, parentFolderId, fieldName_id, fieldName_name, includeFoldersOfNoSubFolder)

    for file in files:
        fileId = file.get(fieldName_id)
        deleteDriveFile(fileId)

def deleteDriveFile(fileId):
    try:
        service.files().delete(fileId = fileId).execute()
    except errors.HttpError as error:
        print("An error occurred: %s" % error)

def getImgUrls(parentFolderId):
    imgFileIds = getImgFileIds(parentFolderId)
    
    imgUrls = []
    for imgFileId in imgFileIds:
        imgUrl = "https://drive.google.com/uc?export=view&id=" + imgFileId
        imgUrls.append(imgUrl)

    return imgUrls

def getImgFileIds(parentFolderId):
    mimeType = MimeType.get("Img")
    fieldName_id = "id"
    fieldName_name = "name"
    includeFoldersOfNoSubFolder = False
    
    infoAry = getInfoAry_filesInFolder(mimeType, parentFolderId, fieldName_id, fieldName_name, includeFoldersOfNoSubFolder)

    imgFileIds = [dic[fieldName_id] for dic in infoAry]

    return imgFileIds

def writeJsonToFile(jsonObj, outputFileName):
    jsonStr = json.dumps(jsonObj)
    text_file = open(outputFileName, "w")
    text_file.write(jsonStr)
    text_file.close()
