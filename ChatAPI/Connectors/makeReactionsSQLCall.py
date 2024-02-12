from Connectors import dbConnector

connection = dbConnector.chatAPIDBConnector()


def postReaction(messageId, userId,emoji):
    sql = f"insert into chatapi.reactions (messageId, userId, symbol) values({messageId}, {userId}, '{emoji}')"
    return connection.insertCall(sql)

def getUserReactionFromMessage(messageId, userId):
    sql = f"select id, UserId, Symbol from chatapi.reactions where archived = false and messageId = {messageId} and userId = {userId}"
    return connection.selectCall(sql)
def getUserReaction(reactionId, userId):
    sql = f"select id, UserId, Symbol from chatapi.reactions where archived = false and id = {reactionId} and userId = {userId}"
    return connection.selectCall(sql)


def getReactions(messageId):
    sql = f"select id, UserId, Symbol from chatapi.reactions where archived = false and messageId = {messageId}"
    return connection.selectCall(sql)

def doesReactionExistWithUserAndMessage(messageId, userId):
    jsonArray = getUserReactionFromMessage(messageId, userId)
    if (len(jsonArray) == 0):
        return False
    return True #id auto_increments, no chance of duplicates

def doesReactionExistWithUser(reactionId, userId):
    jsonArray = getUserReaction(reactionId, userId)
    if (len(jsonArray) == 0):
        return False
    return True #id auto_increments, no chance of duplicates


def getReaction(reactionId):
    sql = f"select id, UserId, Symbol from chatapi.reactions where archived = false and id = {reactionId}"
    return connection.selectCall(sql)

def patchReaction(reactionId, emoji):
    sql = f"update chatapi.reactions set symbol = '{emoji}' where id = {reactionId}"
    return connection.insertCall(sql)


def deleteReaction(reactionId):
    sql = f"update chatapi.reactions set archived = true where id = {reactionId}"
    return connection.insertCall(sql)