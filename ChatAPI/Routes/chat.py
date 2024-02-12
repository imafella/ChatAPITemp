import json

from flask import Blueprint, jsonify, Response, request

from Connectors import makeChatsSQLCall
from Connectors import makeUsersSQLCall
import sys

sys.path.append('../Tools')
from Tools import JsonMethods as jMeth
from Tools import RequestTools as rTools

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat', methods=['GET'])
def getChats():
    #TODO Pagination
    if(jMeth.isFieldPresent(request.headers, "user")):
        jsonArray = makeChatsSQLCall.getAllYourChats(request.headers['user'])
    else:
        jsonArray = makeChatsSQLCall.getAllChats()
    for i, chats in enumerate(jsonArray):
        chatId = chats['chatId']
        jsonArray[i]['Users'] = makeChatsSQLCall.getUsersInChat(chatId)
        jsonArray[i]['ChatName'] = makeChatsSQLCall.getChatName(chatId)[0]['chatname']
        #TODO Get Last Message
    return Response(json.dumps(jsonArray), status=200, mimetype='application/json', content_type='application/json')


@chat_bp.route('/chat', methods=['Post'])
def postChat():
    theRequest = request.json
    chatId = makeChatsSQLCall.postChat()
    for i in theRequest['users']:
        if (makeUsersSQLCall.doesUserExist(i)):
            makeChatsSQLCall.addUserToChat(i, chatId)
        else:
            return Response(f"User {i} does not exist", status=404, mimetype='application/json',
                            content_type='application/json')
    return Response("", status=201, mimetype='application/json', content_type='application/json')


@chat_bp.route('/chat/<chatId>', methods=['GET'])
def getChat(chatId):
    if(not makeChatsSQLCall.doesChatExist(chatId)):
        return Response("", status=404, mimetype='application/json', content_type='application/json')
    jsonArray = {}
    jsonArray['Users'] = makeChatsSQLCall.getUsersInChat(chatId)
    jsonArray['ChatName'] = makeChatsSQLCall.getChatName(chatId)[0]['chatname']
    # TODO Get Last Message

    return Response(json.dumps(jsonArray), status=200, mimetype='application/json', content_type='application/json')


@chat_bp.route('/chat/<chatId>', methods=['PATCH'])
def patchChat(chatId):
    theRequest = request.json
    if (not makeChatsSQLCall.doesChatExist(chatId)):
        return Response("Chat not found", status=404, mimetype='application/json', content_type='application/json')
    makeChatsSQLCall.patchChat(chatId, theRequest)
    return Response('Chat Patched', status=200, mimetype='application/json')


@chat_bp.route('/chat/<chatId>', methods=['Delete'])
def deleteChat(chatId):
    if (not makeChatsSQLCall.doesChatExist(chatId)):
        return Response("Chat not found", status=404, mimetype='application/json', content_type='application/json')
    makeChatsSQLCall.deleteChat(chatId)
    return Response("Chat Deleted", status=200, mimetype='application/json', content_type='application/json')
