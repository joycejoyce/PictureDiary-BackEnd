from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import json

service = None

def getService():
    creds = getCreds()
    
    global service
    service = build('drive', 'v3', credentials=creds)
    
    return service

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
            SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                        'https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/drive.file',
                        'https://www.googleapis.com/auth/drive.appdata']
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

### getInfoAry_filesInFolder() ###
# output:
# [
#     {
#         "id": "0001",
#         "name": "test1"
#     },
#     {
#         "id": "0002",
#         "name": "test2"
#     }
# ]
###
def getInfoAry_filesInFolder(mimeType, parentFolderId, fieldName_id, fieldName_name, includeFoldersOfNoSubFolder):
    print("parentFolderId", parentFolderId)
    queryStr = "mimeType='%s' and parents in '%s'" % (mimeType, parentFolderId)

    response = service.files().list(q = queryStr,
                                spaces = "drive",
                                fields = "files(id, name)").execute()

    files = response.get("files")

    resultJson = json.loads("[]")

    if len(files) == 0:
        msg = "No files found for parentFolderId: " + parentFolderId
        print(msg)
        if includeFoldersOfNoSubFolder:
            obj = {
                "parentFolderId": parentFolderId,
                "msg": msg
            }
            resultJson.append(obj)
    else:
        for file in files:
            id = file.get("id")
            name = file.get("name")

            obj = {
                fieldName_id: id,
                fieldName_name: name
            }

            resultJson.append(obj)

    return resultJson