from Client import app
import Client.util_C as util_C
import Client.cli_to_spec

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
    if name in ['rtt']:
        succeed, spec = getattr(Client.cli_to_spec, name)(args)
    else:
        succeed = False
        spec = 'Test type unsupported.'
    
    if succeed:
        return util_C.json_return(spec)
    else:
        return util_C.bad_request(spec)
