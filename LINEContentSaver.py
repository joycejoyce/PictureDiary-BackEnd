from __future__ import print_function
import os.path
import requests
import json # added
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import FilePathGetter
import FileSaver

app = Flask(__name__)
def main():
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

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

handler = WebhookHandler('2e7ee14868554f9804bc8ef5b0073a41')
@handler.add(MessageEvent)
def handle_message(event):
    print("got event")
    FileSaver.save(event.message)

if __name__ == '__main__':
    main()