import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())
import util
from flask import Flask

app = Flask(__name__)
#app.config['APPLICATION_ROOT'] = util.api_root()

#@app.route('/')
#def hello():
#    return 'Hello The World\n'

from Client.test import *
from Client.task import *

if __name__ == '__main__':
    app.run(debug=True, port=80)