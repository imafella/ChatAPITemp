from Connectors import dbConnector

connection = dbConnector.chatAPIDBConnector()

def getAllUsers(queryParams: dict):
    queryString = ''
    if(queryParams['search'] is not None):
        queryString+= f" and username like '%{queryParams['search']}%' or email like '%{queryParams['search']}%'"
    if((queryParams['offset'] is not None) and (queryParams['limit'] is not None)):
        queryString+= f" limit {queryParams['offset']}, {queryParams['limit']}"
    elif(queryParams['limit'] is not None):
        queryString+= f" limit {queryParams['limit']}"
    sql = "SELECT id, username, email FROM chatAPI.USERS where archived=false"+queryString
    return connection.selectCall(sql)


def postUser(dict):
    sql = f"INSERT INTO USERS(username, email) Values('{sanatizeInput(dict['name'])}','{sanatizeInput(dict['email'])}')"
    return connection.insertCall(sql)
def sanatizeInput(input):
    input = input.split(';',1)[0] #Removes any potential malicious sql injections.
    return input


def getUser(userId):
    sql = f"SELECT id, username, email FROM chatAPI.USERS where archived=false and id = {userId}"
    return connection.selectCall(sql)


def patchUser(userId, theRequest):
    up = "Update chatAPI.USERS set "
    if('name' in theRequest):
        up+= f" username = '{theRequest['name']}',"
    if('email' in theRequest):
        up+= f" email = '{theRequest['email']}',"
    if('isAdmin' in theRequest):
        up+= f" isAdmin = {theRequest['isAdmin']},"
    sql = f"{up[:-1]} where id = {userId} and archived = false"
    return connection.insertCall(sql)


def deleteUser(userId):
    sql = f"Update chatAPI.USERS set archived = true where id = {userId}"
    connection.insertCall(sql)
    sql = f"Update chatAPI.messages set archived = true where userid = {userId}"
    return connection.insertCall(sql)

def doesUserExist(userId):
    jsonArray = getUser(userId)
    if (len(jsonArray) == 0):
        return False
    return True #id auto_increments, no chance of duplicates