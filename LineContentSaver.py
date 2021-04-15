from linebot import LineBotApi
import FilePathGetter
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import FilePathProcessor
from GoogleDriveProcessor import getService
from GlobalVar import LineContentFolderId

service = None

def save(message):
    global service
    service = getService()
    
    msgType = message.type
    localFilePath = getFilePath(message)
    saveToLocal(message, localFilePath, msgType)
    saveToCloud(localFilePath)
    
line_bot_api = LineBotApi('dzuf4ok7JghxVZh1Ua+V2vYDUmGnQXW/L5v5yivAzCNae2STLMjhonxgdt/rDh6DKgtPuc/yRFVfzgqrcZPJc3vCQxoQC8TzQWBX0mBdtixudw50CiM7k4kJaYcMq442zV6Sx/WE+cjbzoD0hreLcwdB04t89/1O/w1cDnyilFU=')
def saveToLocal(message, filePath, msgType):
    if msgType == "text":
        message_text = message.text
        fd = open(filePath, "a")
        fd.write(message_text)
    elif msgType == "image":
        message_content = line_bot_api.get_message_content(message.id)
        with open(filePath, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
    elif msgType == "video":
        message_content = line_bot_api.get_message_content(message.id)
        with open(filePath, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
                
    print("saveToLocal [%s] done" % filePath)

def getFilePath(message):
    filePath = FilePathGetter.get(message)
    return filePath

def getMimeType(localFilePath):
    fileExtension = FilePathProcessor.getFileExtension(localFilePath)

    mimeType = ""

    if fileExtension == "txt":
        mimeType = "text/plain"
    elif fileExtension == "jpg":
        mimeType = "image/jpeg"
    elif fileExtension == "mp4":
        mimeType = "video/mp4"
    else:
        raise Exception("Unexpeted fileExtension: [%s]" % fileExtension)

    print("mimeType: [%s]" % mimeType)

    return mimeType

def saveToCloud(localFilePath):
    mimeType = getMimeType(localFilePath)
    uploadFile(service, localFilePath, mimeType)

def uploadFile(service, localFilePath, mimeType):
    folderId_root = LineContentFolderId

    folderName = FilePathProcessor.getFolderName(localFilePath)
    print("folderName: [%s]" % folderName)

    folderId_Date = getFileId(service, folderName, folderId_root)
    print("folderId_Date (existed): [%s]" % folderId_Date)

    if not folderId_Date:
        folderId_Date = createFolder(service, folderName, folderId_root)        
        print ("folderId_Date (new-created): [%s]" % folderId_Date)

    fileName = FilePathProcessor.getFileName(localFilePath)
    print("fileName: [%s]" % fileName)

    createFile(service, folderName, fileName, mimeType, folderId_Date)

def getFileId(service, folderName, folderId_root):
    queryStr = "mimeType='application/vnd.google-apps.folder' and name='%s' and parents in '%s'" % (folderName, folderId_root)
    page_token = None
    response = service.files().list(q=queryStr,
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=page_token).execute()
    files = response.get('files')
    if len(files) > 0:
        return files[0].get('id')
    else:
        return None

def createFolder(service, folderName, folderId_root):
    file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folderId_root]
    }
    file = service.files().create(body=file_metadata, fields='id').execute()

    id = file.get('id')

    return id

def createFile(service, folderName, fileName, mimeType, folderId_parent):
    filePath = folderName + "/" + fileName
    fileMetaData = {
        'name': fileName,
        'mimeType': mimeType,
        'parents': [folderId_parent]
    }
    file = MediaFileUpload(filePath,
                            mimetype=mimeType,
                            resumable=True)
    request = service.files().create(body=fileMetaData, media_body=file, fields='id').execute()

    print ("File ID: [%s]" % request.get("id"))
    print ("uploadFile [%s] done" % filePath)