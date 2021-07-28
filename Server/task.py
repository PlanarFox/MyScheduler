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
# myScheduler server address. Only localhost is supported right now 

if not util.api_has_MyScheduler(assist):
    raise ValueError('Assist Server Error.')

# command line arguments validationand specing
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


task['test']['spec'] = raw_spec

if task['test']['spec'].get('participants', None) is None:
    task['test']['spec']['participants'] = [util.api_local_host()]
    # single participant only right now
    # participant list should be maintained by assist server eventually


for participant in task['test']['spec']['participants']:
    if not util.api_has_MyScheduler(participant):
        raise ValueError('Participant hasn\'t install MyScheduler yet.')


#Give the task to the participant(s). No multi-participants considiered.
for participant in task['test']['spec']['participants']:
    task_url = util.api_url(participant, '/tasks')
    print('get task url:', task_url)
    status, task_url = url.url_post(task_url, data=task)

if status != 200:
    raise ValueError('Task post failed:\n' + task_url)
else:
    print('task url:', task_url)

