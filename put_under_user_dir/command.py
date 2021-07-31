import subprocess
import json
import sys

def run(task_json):
    task_json = json.loads(task_json)

    if task_json['test']['type'] == 'rtt':
        f = rtt

    return (f(task_json))

def rtt(data):
    dest = data['test']['spec'].get('dest', '-')
    try:
        if dest == '-':
            raise ValueError('Destination not found')
    except Exception as e:
        raise e
    
    command = ['ping', '-n', '-c', '4']
    command.append(dest)
    proc = subprocess.run(command, stdout=subprocess.PIPE, timeout=7)
    if proc.returncode == 0:
        return proc.stdout.decode('utf-8')
    else:
        raise ValueError('ping failed')

