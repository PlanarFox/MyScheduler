import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())
import myjson
import url
import argparse
import util

parser = argparse.ArgumentParser(description='run task with myScheduler')
parser.add_argument('--test', action='store_true', help='to check if the argparse is working')
args, remain = parser.parse_known_args()

if args.test:
    print('argparse working')

print('remaining options:')
print(remain)

task = {
    'test': {
        'spec': {}
    }
}

if len(remain) > 0:
    test_arg = remain.pop(0)
    if test_arg == 'rtt':
        task['test']['type'] = test_arg
    else:
        raise ValueError('No such test type.')

test_type = task['test'].get('type', '-')

if test_type == '-':
    raise ValueError('No test type specified.')

assist = util.api_local_host()

if not util.api_has_MyScheduler(assist):
    raise ValueError('Assist Server Error.')

spec_url = util.api_url_hostport(assist, path = 'tests/' + test_type + '/spec')
status, raw_spec = url.url_get(
    spec_url,
    params={'args': myjson.json_dump(remain)},
)

if status == 200:
    print('succeed')
    print(raw_spec)
else:
    print(status)
    print(raw_spec)
