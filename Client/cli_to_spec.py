import argparse
import myjson

def rtt(cli_list):
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