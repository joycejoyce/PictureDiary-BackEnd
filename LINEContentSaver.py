from __future__ import print_function
import pickle
import os.path
import requests
import json # added
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import FileNameGetter

def main():
    fileExtension = "txt"
    fileName = FileNameGetter.get(fileExtension)
    print("got fileName: " + fileName)
    # port = int(os.environ.get('PORT', 80))
    # app.run(host='0.0.0.0', port=port)

app = Flask(__name__)
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

line_bot_api = LineBotApi('dzuf4ok7JghxVZh1Ua+V2vYDUmGnQXW/L5v5yivAzCNae2STLMjhonxgdt/rDh6DKgtPuc/yRFVfzgqrcZPJc3vCQxoQC8TzQWBX0mBdtixudw50CiM7k4kJaYcMq442zV6Sx/WE+cjbzoD0hreLcwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2e7ee14868554f9804bc8ef5b0073a41')
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type

    if message_type == "text":
        message_text = event.message.text
        # reply_token = event.reply_token
        # line_bot_api.reply_message(reply_token, TextSendMessage(text = message_text))
    elif message_type == "image":
        message_content = line_bot_api.get_message_content(event.message.id)
        with open("test.jpg", 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
    elif message_type == "video":
        message_content = line_bot_api.get_message_content(event.message.id)
        with open("test.mp4", 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

def saveContents(fileName, mimeType):
    creds = getCreds()
    service = runService(creds)
    uploadFile(service, fileName, mimeType)

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
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def runService(creds):
    service = build('drive', 'v3', credentials=creds)
    return service

def uploadFile(service, fileName, mimeType):
    file_metadata = {
        'name': fileName,
        'mimeType': mimeType
    }
    media = MediaFileUpload(fileName,
                            mimetype=mimeType,
                            resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print ('File ID: ' + file.get('id'))

if __name__ == '__main__':
    main()