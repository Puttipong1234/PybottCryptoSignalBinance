from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from get_all_symbols import start_screener , start_screener_all

sched = BlockingScheduler()

from datetime import datetime
    


@sched.scheduled_job('interval', hours=4)
def job_start_screener():
    start_screener()
    
@sched.scheduled_job('interval', hours=24)
def job_start_screener_all():
    start_screener_all()
    
@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes. หลอก heroku')


    
if __name__ == '__main__':
    start_screener()
    start_screener_all()
    sched.start()
    