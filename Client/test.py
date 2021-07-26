from Client import app
import util_C # comment when coding
#from . import util_C # comment when running
from flask import Response

@app.route('/myscheduler')
def hello():
    return 'Here is MyScheduler\n'

@app.route("/myscheduler/tests/<name>/spec", methods=["GET"])
def spec_to_cli(name):
    args = util_C.arg_json('args')
    for arg in args:
      if not ( isinstance(arg, str)
               or isinstance(arg, int)
               or isinstance(arg, float) ):
         return 
    args = [ str(arg) for arg in args ]
    if name == 'rtt':
        succeed, spec = util_C.rtt_cli_to_spec(args)
    else:
        succeed = False
        spec = 'Test type unsupported.'
    
    if succeed:
        return util_C.json_return(spec)
    else:
        return util_C.bad_request(spec)
