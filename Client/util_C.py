import os
import sys
from urllib import parse
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())
from flask import request
import myjson
import argparse
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

def rtt_cli_to_spec(cli_list):
    parser = argparse.ArgumentParser(description='rtt spec arg parse')
    parser.add_argument('--dest', type=str, help='rtt destination host')
    args, remain = parser.parse_known_args(cli_list)

    result = {}

    if args.dest is None:
        return False, 'No destination host has got.'
    
    if len(remain) > 0:
        return False, 'Unsupported arguments detected.'

    result['dest'] = args.dest

    return True, myjson.json_dump(result)

def json_return(data):
    return Response(data + '\n', mimetype='application/json')

def bad_request(message='Bad Request'):
    return Response(message + '\n', status=400, mimetype='text/plain')
    
    