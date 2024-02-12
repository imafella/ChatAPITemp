from Connectors import dbConnector

connection = dbConnector.chatAPIDBConnector()


def postMessage(chatId, userId, messageBody):
    # TODO sanatize messageBody but lack time to do so
    sql = f" Insert into chatapi.messages (chatId, userId, messageBody) values ({chatId}, {userId}, '{messageBody}')"
    return connection.insertCall(sql)


def postMedia(file, filetype, messageId):
    sql = f"update chatapi.messages set media = {file}, mediaType = '{filetype}' where id = {messageId}"
    return connection.insertCall(sql)


def getMessages(chatId):
    sql = f"Select id, userid, messagebody, media, mediatype, dateposted from chatapi.messages where archived = false and chatId = {chatId}"
    return connection.selectCall(sql)


def getLastMessage(chatId):
    sql = f"Select id, userid, messagebody, media, mediatype, dateposted from chatapi.messages where archived = false and chatId = {chatId} limit 1 order by id desc"
    return connection.selectCall(sql)


def getMessage(messageId):
    sql = f"Select id, userid, messagebody, media, mediatype, dateposted from chatapi.messages where archived = false and id = {messageId}"
    return connection.selectCall(sql)


def doesMessageExist(messageId):
    jsonArray = getMessage(messageId)
    if (len(jsonArray) == 0):
        return False
    return True  # id auto_increments, no chance of duplicates


def getMessageAndUser(messageId, userId):
    sql = f"Select id, userid, messagebody, media, mediatype, dateposted from chatapi.messages where archived = false and id = {messageId} and userid = {userId}"
    return connection.selectCall(sql)


def patchMessageBody(messageBody, messageId):
    sql = f"update chatapi.messages set messagebody = '{messageBody}' where id = {messageId}"
    return connection.insertCall(sql)


def patchMessageMedia(messageId, media, mediaType):
    sql = f"update chatapi.messages set media = '{media}', mediatype = '{mediaType}' where id = {messageId}"
    return connection.insertCall(sql)


def deleteMessage(messageId):
    sql = f"update chatapi.messages set archived = true where id = {messageId}"
    return connection.insertCall(sql)


def doesMessageExistWithUser(messageId, userId):
    jsonArray = getMessageAndUser(messageId, userId)
    if (len(jsonArray) == 0):
        return False
    return True  # id auto_increments, no chance of duplicates
