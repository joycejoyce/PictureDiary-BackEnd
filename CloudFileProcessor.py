from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import ntpath
import os
import pickle
import FilePathProcessor

def save(localFilePath):
    mimeType = getMimeType(localFilePath)
    saveToCloud(localFilePath, mimeType)

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

def saveToCloud(localFilePath, mimeType):
    creds = getCreds()
    service = runService(creds)
    uploadFile(service, localFilePath, mimeType)

def getCreds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.appdata']
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def runService(creds):
    service = build('drive', 'v3', credentials=creds)
    return service

def uploadFile(service, localFilePath, mimeType):
    folderId_root = "1cqhxLGtfRJ9kRPbhP9gDE8alBMWL3gco" # "LineContent" folder ID

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