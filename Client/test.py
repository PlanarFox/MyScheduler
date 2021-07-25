from Client import app

@app.route('/myscheduler')
def hello():
    return 'Here is MyScheduler\n'