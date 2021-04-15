from __future__ import print_function
import os.path
import requests
import json # added
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import FilePathGetter
import LineContentSaver
import LineContentJsonGenerator
from GlobalVar import RetMsg_OK

app = Flask(__name__)
def main():
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: [%s]" % body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return RetMsg_OK

handler = WebhookHandler('2e7ee14868554f9804bc8ef5b0073a41')
@handler.add(MessageEvent)
def handle_message(event):
    LineContentSaver.save(event.message)

@app.route("/genAllJson")
def genAllJson():
    LineContentJsonGenerator.gen()
    return RetMsg_OK

if __name__ == '__main__':
    main()