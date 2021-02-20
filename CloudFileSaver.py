from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import ntpath
import os
import pickle

def save(localFilePath):
    mimeType = getMimeType(localFilePath)
    saveToCloud(localFilePath, mimeType)

def getMimeType(localFilePath):
    fileExtension = getFileExtension(localFilePath)

    mimeType = ""

    if fileExtension == "txt":
        mimeType = "text/plain"
    elif fileExtension == "jpg":
        mimeType = "image/jpeg"
    elif fileExtension == "mp4":
        mimeType = "video/mp4"
    else:
        raise Exception("Unexpeted fileExtension: " + fileExtension)

    print("mimeType: " + mimeType)

    return mimeType

def getFileExtension(localFilePath):
    fileName, fileExtension = os.path.splitext(localFilePath)
    fileExtension = fileExtension[1:]
    print("fileExtension: " + fileExtension)
    return fileExtension

def saveToCloud(localFilePath, mimeType):
    fileName = getFileName(localFilePath)
    creds = getCreds()
    service = runService(creds)
    uploadFile(service, fileName, localFilePath, mimeType)

def getFileName(localFilePath):
    fileName = ntpath.basename(localFilePath)
    print("fileName: " + fileName)
    return fileName

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

def uploadFile(service, fileName, filePath, mimeType):
    fileMetaData = {
        'name': fileName,
        'mimeType': mimeType
    }
    media = MediaFileUpload(filePath,
                            mimetype=mimeType,
                            resumable=True)
    request = service.files().create(body=fileMetaData, media_body=media, fields='id').execute()

    print ("File ID: " + request.get('id'))
    print ("uploadFile(" + fileName + ") done")
    