import json

from flask import Blueprint, jsonify, Response, request

from Connectors import makeChatsSQLCall
from Connectors import makeUsersSQLCall
from Connectors import makeMessagesSQLCall
import sys

sys.path.append('../Tools')
from Tools import JsonMethods as jMeth
from Tools import RequestTools as rTools

message_bp = Blueprint('message', __name__)


@message_bp.route('/chat/<chatId>/message', methods=['GET'])
def getMessages(chatId):
    #TODO pagination
    jsonArray = makeMessagesSQLCall.getMessages(chatId)
    return Response(json.dumps(jsonArray, default=str), status=200, mimetype='application/json', content_type='application/json')


@message_bp.route('/chat/<chatId>/message', methods=['Post'])
def postMessage(chatId):
    # Verification of details block
    if ((not (jMeth.isFieldPresent(request.headers, "user")))):
        return Response("Bad Request: Missing user header", status=400, mimetype='application/json',
                        content_type='application/json')
    userId = request.headers['user']
    if((not (makeChatsSQLCall.doesChatExist(chatId))) or (not (makeUsersSQLCall.doesUserExist(userId)))):
        return Response("Chat or User does not exist", status=404, mimetype='application/json',
                        content_type='application/json')
    theRequest = request.json
    if ((not (jMeth.isFieldPresent(theRequest, "MessageBody")))):
        return Response("Bad Request: Missing MessageBody", status=400, mimetype='application/json',
                        content_type='application/json')

    messageBody = theRequest["MessageBody"]
    messageId = makeMessagesSQLCall.postMessage(chatId, userId, messageBody)
    if(jMeth.isFieldPresent(theRequest, "Media")):
        #The Call for handling Media files, Untested.
        # TODO put limit on file size
        makeMessagesSQLCall.postMedia(theRequest['Media'], theRequest['MediaType'], messageId)
    return Response("Message Posted", status=201, mimetype='application/json', content_type='application/json')


@message_bp.route('/message/<messageId>', methods=['GET'])
def getMessage(chatId, messageId):
    jsonArray = makeMessagesSQLCall.getMessage(messageId)
    return Response(json.dumps(jsonArray, default=str), status=200, mimetype='application/json', content_type='application/json')


@message_bp.route('/message/<messageId>', methods=['PATCH'])
def patchMessage(messageId):
    if ((not (jMeth.isFieldPresent(request.headers, "user")))):
        return Response("Bad Request: Missing user header", status=400, mimetype='application/json',
                        content_type='application/json')
    userId = request.headers['user']
    if(not makeMessagesSQLCall.doesMessageExistWithUser(messageId, userId)):
        return Response("Message with User not found.", status=404, mimetype='application/json', content_type='application/json')

    theRequest= request.json
    if (jMeth.isFieldPresent(theRequest, "MessageBody")):
        makeMessagesSQLCall.patchMessageBody(theRequest['MessageBody'], messageId)
    if (jMeth.isFieldPresent(theRequest, "Media")):
        #Not Tested
        makeMessagesSQLCall.patchMessageBody(messageId, theRequest["Media"], theRequest["MediaType"])
    return Response(f"Patched message", status=200, mimetype='application/json', content_type='application/json')


@message_bp.route('/message/<messageId>', methods=['DELETE'])
def deleteMessage(messageId):
    if ((not (jMeth.isFieldPresent(request.headers, "user")))):
        return Response("Bad Request: Missing user header", status=400, mimetype='application/json',
                        content_type='application/json')
    userId = request.headers['user']
    if(not makeMessagesSQLCall.doesMessageExistWithUser(messageId, userId)):
        return Response("Message with User not found.", status=404, mimetype='application/json', content_type='application/json')
    makeMessagesSQLCall.deleteMessage(messageId)
    return Response("Message Deleted", status=200, mimetype='application/json', content_type='application/json')
