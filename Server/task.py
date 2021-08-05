import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())
import requests
import argparse
import util
import time
import myjson

parser = argparse.ArgumentParser(description='run task with myScheduler')
parser.add_argument('--test', action='store_true', help='to check if the argparse is working')
parser.add_argument('--host', type=str, help='assist server address')
parser.add_argument('--port', type=str, default='80', help='assist server port')
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

if args.host is None:
    assist = util.api_local_host()
else:
    assist = args.host + ':' + args.port
# myScheduler server address. Only localhost is supported right now 

if not util.api_has_MyScheduler(assist):
    raise ValueError('Assist Server Error.')

# command line arguments validationand specing
spec_url = util.api_url_hostport(assist, path = 'tests/' + test_type + '/spec')

r = requests.get(url = spec_url, params={'args': myjson.json_dump(remain)})
status = r.status_code
raw_spec = r.json()

if status == 200:
    print('succeed')
    print(raw_spec)
else:
    print(status)
    print(raw_spec)


task['test']['spec'] = raw_spec

if task['test']['spec'].get('participants', None) is None:
    task['test']['spec']['participants'] = [assist]
    # single participant only right now
    # participant list should be maintained by assist server eventually


for participant in task['test']['spec']['participants']:
    if not util.api_has_MyScheduler(participant):
        raise ValueError('Participant hasn\'t install MyScheduler yet.')


#Give the task to the participant(s). No multi-participants considiered.
for participant in task['test']['spec']['participants']:
    task_url = util.api_url(participant, '/tasks')
    print('get task url:', task_url)
    r = requests.post(url=task_url, json=task)
    status = r.status_code
    task_url = r.text[1:-2]

if status != 200:
    raise ValueError('Task post failed:\n' + task_url)
else:
    print('task url:', task_url)


print('fetching the running result')
while True:
    time.sleep(1.0)
    r = requests.get(url = task_url)
    status = r.status_code
    result = r.text[1:-2]
    if status == 400:
        print('fetching result failed,: ', result)
        print('retrying...')
    else:
        print(result)
        break
