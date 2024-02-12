from Connectors import dbConnector

connection = dbConnector.chatAPIDBConnector()


def getAllYourChats(UserId):  # returns ID of all unarchived Chats that the User is in.
    sql = f"Select chatId from chatapi.usersinchat where archived=false and UserId = {UserId}"
    return connection.selectCall(sql)


def getUsersInChat(chatId):
    sql = ("select users.id, users.username, users.email  from chatapi.users "
           + "left join chatapi.usersinchat on chatapi.users.id = chatapi.usersinchat.UserId "
           + "left join chatapi.chats on chatapi.chats.id = chatapi.usersinchat.chatId "
           + "where chatapi.users.archived = false and chatapi.usersinchat.archived = false "
           + f"and chatapi.chats.archived = false and chatapi.usersinchat.chatId = {chatId}")
    return connection.selectCall(sql)

def getUserIDsInChat(chatId):
    sql = ("select users.id as id from chatapi.users "
           + "left join chatapi.usersinchat on chatapi.users.id = chatapi.usersinchat.UserId "
           + "left join chatapi.chats on chatapi.chats.id = chatapi.usersinchat.chatId "
           + "where chatapi.users.archived = false and chatapi.usersinchat.archived = false "
           + f"and chatapi.chats.archived = false and chatapi.usersinchat.chatId = {chatId}")
    return connection.selectCall(sql)
def getChatName(chatId):
    sql= f"Select chatname from chatapi.chats where archived = false and id = {chatId}"
    return connection.selectCall(sql)


def postChat():
    sql = f"Insert into chatapi.chats () values ()"
    return connection.insertCall(sql)


def addUserToChat(userId, chatId):
    sql = f"Insert into chatapi.usersinchat (UserId, ChatId) values ({userId}, {chatId})"
    return connection.insertCall(sql)


def getAllChats():  # returns ID of all unarchived Chats.
    sql = f"Select Distinct chatId from chatapi.usersinchat where archived=false"
    return connection.selectCall(sql)


def getChat(chatId):
    sql = f"Select id from chatapi.chats where archived=false and id = {chatId}"
    return connection.selectCall(sql)

def patchUserOutOfChat(chatId, userId):
    sql = f"update chatapi.usersinchat set archived = true where userid = {userId} and chatId = {chatId}"
    return connection.insertCall(sql)
def patchNameOfChat(chatId, chatname):
    sql = f"update chatapi.chats set chatname = '{chatname}' where id = {chatId} and archived = false"
    return connection.insertCall(sql)



def doesChatExist(chatId):
    jsonArray = getChat(chatId)
    if (len(jsonArray) == 0):
        return False
    return True #id auto_increments, no chance of duplicates


def patchChat(chatId, theRequest):
    #I hate how i wrote this. There has to be a smarter and simpler way to find the
    # delta and add the new and remove the old
    if('ChatName' in theRequest):
        patchNameOfChat(chatId, theRequest['ChatName'])
    if('Users' in theRequest):
        currentUsers = getUserIDsInChat(chatId)
        arrayOfCurrentUsers=[]
        arrayofNewUsers = theRequest['Users']
        for i, user in enumerate(currentUsers):
            id = user['id']
            arrayOfCurrentUsers.append(id)
            if(not (id in arrayofNewUsers)):
                patchUserOutOfChat(chatId, id)
        for user in arrayofNewUsers:
            if(not(user in arrayOfCurrentUsers)):
                addUserToChat(user, chatId)


def deleteChat(chatId):
    # Archives the chat and then the link between users and chats
    sql = f"update chatapi.chats set archived = true where id = {chatId}"
    connection.insertCall(sql)
    sql = f"update chatapi.usersinchat set archived = true where chatId = {chatId}"
    connection.insertCall(sql)
    sql = f"update chatapi.messages set archived = true where chatid = {chatId}"
    connection.insertCall(sql)
    return connection.insertCall(sql)
