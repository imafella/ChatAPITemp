import json

from flask import Blueprint, jsonify, Response, request

from Connectors import makeUsersSQLCall
import sys

sys.path.append('../Tools')
from Tools import JsonMethods as jMeth
from Tools import RequestTools as rTools

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
def getUsers():
    queryParams = rTools.getQueryParams(request)
    jsonArray = makeUsersSQLCall.getAllUsers(queryParams)
    if (jsonArray == 'null'):
        jsonArray = ''
    return Response(json.dumps(jsonArray), status=200, mimetype='application/json', content_type='application/json')


@user_bp.route('/user', methods=['POST'])
def postUser():
    theRequest = request.json
    if (jMeth.isFieldPresent(theRequest, 'name') and jMeth.isFieldPresent(theRequest, 'email')):
        makeUsersSQLCall.postUser(theRequest)
        return Response('User Created', status=201, mimetype='application/json', content_type='application/json')
    else:
        return Response('Bad Request: Missing Fields, needed name & email', status=400, mimetype='application/json')
        # I would like to have a more detailed response with specifying the missing field... but time is of the essence


@user_bp.route('/user/<userId>', methods=['GET'])
def getUser(userId):
    jsonArray = makeUsersSQLCall.getUser(userId)
    if (len(jsonArray) == 0):
        return Response("User not found", status=404, mimetype='application/json', content_type='application/json')
    return Response(json.dumps(jsonArray[0]), status=200, mimetype='application/json', content_type='application/json')

@user_bp.route('/user/<userId>', methods=['PATCH'])
def patchUser(userId):
    theRequest = request.json
    if(not makeUsersSQLCall.doesUserExist(userId)):
        return Response("User not found", status=404, mimetype='application/json', content_type='application/json')
    makeUsersSQLCall.patchUser(userId, theRequest)
    return Response('User Patched', status=200, mimetype='application/json')

@user_bp.route('/user/<userId>', methods=['DELETE'])
def deleteUser(userId):
    if (not makeUsersSQLCall.doesUserExist(userId)):
        return Response("User not found", status=404, mimetype='application/json', content_type='application/json')
    makeUsersSQLCall.deleteUser(userId)
    return Response('User Deleted', status=200, mimetype='application/json')

# TODO if time allows
# @user_bp.route('/user/{userId}/chat', methods=['GET'])
# def getUserChat(userId):
#    return Response(jsonArray, status=200, mimetype='application/json')


