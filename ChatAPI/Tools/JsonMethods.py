import json

def isFieldPresent(dict, field):
    try:
        dict[field]
        return True
    except:
        return False
