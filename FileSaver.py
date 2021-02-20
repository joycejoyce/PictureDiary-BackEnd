from linebot import LineBotApi
import FilePathGetter
import CloudFileSaver

def save(message):
    print("got message")
    msgType = message.type
    localFilePath = getFilePath(msgType)
    saveToLocal(message, localFilePath, msgType)
    saveToCloud(localFilePath)
    
line_bot_api = LineBotApi('dzuf4ok7JghxVZh1Ua+V2vYDUmGnQXW/L5v5yivAzCNae2STLMjhonxgdt/rDh6DKgtPuc/yRFVfzgqrcZPJc3vCQxoQC8TzQWBX0mBdtixudw50CiM7k4kJaYcMq442zV6Sx/WE+cjbzoD0hreLcwdB04t89/1O/w1cDnyilFU=')
def saveToLocal(message, filePath, msgType):
    print("saveToLocal(" + filePath + ")")
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
    print("saveToLocal [" + filePath + "] done")

def getFilePath(msgType):
    if msgType == "text":
        fileExtension = "txt"
    elif msgType == "image":
        fileExtension = "jpg"
    elif msgType == "video":
        fileExtension = "mp4"

    filePath = FilePathGetter.get(fileExtension)
    print("filePath: " + filePath)

    return filePath

def saveToCloud(localFilePath):
    print("saveToCloud(" + localFilePath + ")")
    CloudFileSaver.save(localFilePath)