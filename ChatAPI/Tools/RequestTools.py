from flask import request

def getQueryParams(theRequest: request):
    params = {}
    params['search'] = request.args.get('search')
    params['limit'] = request.args.get('limit')
    params['offset'] = request.args.get('offset')
    return params