from linebot import LineBotApi
import FilePathGetter
import CloudFileSaver

def save(message):
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

def saveToCloud(localFilePath):
    CloudFileSaver.save(localFilePath)