from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from get_all_symbols import start_screener , start_screener_all

sched = BlockingScheduler()

from datetime import datetime
from flask import Flask

app = Flask(__name__)

    


@sched.scheduled_job('interval', hours=4)
def job_start_screener():
    start_screener()
    
@sched.scheduled_job('interval', hours=24)
def job_start_screener_all():
    start_screener_all()
    
@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes. หลอก heroku')
    

@app.route("/start_screener")
def noti1():
    start_screener()
    return "200"

@app.route("/start_screener_all")
def noti2():
    start_screener_all()
    return "200"

    
if __name__ == '__main__':
    app.run(port=200,use_reloader=False)
    
    # start_screener()
    # start_screener_all()
    # sched.start()
    