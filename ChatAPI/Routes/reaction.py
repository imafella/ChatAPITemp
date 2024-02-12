import json

from flask import Blueprint, jsonify, Response, request

from Connectors import makeChatsSQLCall
from Connectors import makeUsersSQLCall
from Connectors import makeMessagesSQLCall
from Connectors import makeReactionsSQLCall
import sys

sys.path.append('../Tools')
from Tools import JsonMethods as jMeth
from Tools import RequestTools as rTools

reaction_bp = Blueprint('reaction', __name__)


@reaction_bp.route('/message/<messageId>/reaction', methods=['GET'])
def getReactions(messageId):
    jsonArray = makeReactionsSQLCall.getReactions(messageId)
    return Response(json.dumps(jsonArray), status=200, mimetype='application/json', content_type='application/json')


@reaction_bp.route('/message/<messageId>/reaction', methods=['POST'])
def postReactions(messageId):
    if not (jMeth.isFieldPresent(request.headers, "user")):
        return Response("Bad Request: Missing user header", status=400, mimetype='application/json',
                        content_type='application/json')
    userId = request.headers['user']
    if (not (makeMessagesSQLCall.doesMessageExist(messageId))) or (not (makeUsersSQLCall.doesUserExist(userId))):
        return Response("Message or User does not exist", status=404, mimetype='application/json',
                        content_type='application/json')
    theRequest = request.json
    if not jMeth.isFieldPresent(theRequest, 'Symbol'):
        return Response("Bad Request: Missing Symbol field", status=400, mimetype='application/json',
                        content_type='application/json')
    if makeReactionsSQLCall.doesReactionExistWithUserAndMessage(messageId, userId):
        return Response("Bad Request: Reaction already made", status=400, mimetype='application/json',
                        content_type='application/json')
    makeReactionsSQLCall.postReaction(messageId, userId, theRequest['Symbol'])
    return Response("Posted reaction", status=201, mimetype='application/json', content_type='application/json')


@reaction_bp.route('/reaction/<reactionId>', methods=['GET'])
def getReaction(reactionId):
    jsonArray = makeReactionsSQLCall.getReaction(reactionId)
    return Response(json.dumps(jsonArray), status=200, mimetype='application/json', content_type='application/json')


@reaction_bp.route('/reaction/<reactionId>', methods=['PATCH'])
def patchReaction(reactionId):
    if not (jMeth.isFieldPresent(request.headers, "user")):
        return Response("Bad Request: Missing user header", status=400, mimetype='application/json',
                        content_type='application/json')
    userId = request.headers['user']
    if (not (makeReactionsSQLCall.doesReactionExistWithUser(reactionId, userId))) or (not (makeUsersSQLCall.doesUserExist(userId))):
        return Response("Reaction or User does not exist", status=404, mimetype='application/json',
                        content_type='application/json')
    theRequest = request.json
    if not jMeth.isFieldPresent(theRequest, 'Symbol'):
        return Response("Bad Request: Missing Symbol field", status=400, mimetype='application/json',
                        content_type='application/json')
    makeReactionsSQLCall.patchReaction(reactionId, theRequest['Symbol'])
    return Response("Patched Reaction", status=200, mimetype='application/json',
                    content_type='application/json')


@reaction_bp.route('/reaction/<reactionId>', methods=['DELETE'])
def deleteReaction(reactionId):
    if not (jMeth.isFieldPresent(request.headers, "user")):
        return Response("Bad Request: Missing user header", status=400, mimetype='application/json',
                        content_type='application/json')
    userId = request.headers['user']
    if (not (makeReactionsSQLCall.doesReactionExistWithUser(reactionId, userId))) or (not (makeUsersSQLCall.doesUserExist(userId))):
        return Response("Reaction or User does not exist", status=404, mimetype='application/json',
                        content_type='application/json')
    makeReactionsSQLCall.deleteReaction(reactionId)
    return Response("Reaction Deleted", status=200, mimetype='application/json',
                    content_type='application/json')
