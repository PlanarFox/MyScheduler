import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())
from flask import request
import myjson
from flask import Response

def arg_json(name):
    arg = request.args.get(name)
    if arg is None:
        return None
    json = myjson.json_load(arg)
    return json

def spec_is_valid(spec):
    # no check for now
    return (True, 'OK')


def json_return(data):
    return Response(data + '\n', mimetype='application/json')

def bad_request(message='Bad Request'):
    return Response(message + '\n', status=400, mimetype='text/plain')
    
def ok(message="OK", mimetype=None):
    return Response(message + '\n', status=200, mimetype=mimetype)

def ok_json(data=None):
    text = myjson.json_dump(data)
    return Response(text + '\n', mimetype='application/json')
    