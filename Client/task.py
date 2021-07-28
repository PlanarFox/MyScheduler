import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())
from Client import app
import Client.util_C as util_C
import Client.spec_is_valid
import myjson
from flask import request
import Client.db as db

@app.route('/myscheduler/tasks', methods=['POST'])
def create_task():
    data = request.data.decode('ascii')
    try:
        task = myjson.json_load(data)
    except ValueError as ex:
        return util_C.bad_request('Invalid task specification: %s' % (str(ex),))

    valid, message = getattr(Client.spec_is_valid, task['test']['type'])(task)

    if not valid:
        return util_C.bad_request('Invalid task specification: %s' % (message))

    conn = db.connect_db()
    if not conn:
        return util_C.bad_request('Database connection failed')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT task_post(%s::jsonb, %s)', \
                        (myjson.json_dump(task), 'True'))
    except Exception as e:
        return util_C.bad_request('Database insert error: %s' % (str(e),))
    uuid = cursor.fetchall()[0][0]
    db.close_db(conn)
    
    task_url = "%s/%s" % (request.base_url, uuid)

    return util_C.ok_json(task_url)
    
    
    

    

    