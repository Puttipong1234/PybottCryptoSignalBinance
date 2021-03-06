from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from get_all_symbols import start_screener , start_screener_all
from user_detail import get_holding_performance

sched = BlockingScheduler()
#test
from datetime import datetime
from flask import Flask , render_template , redirect, url_for, request , jsonify , make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



@sched.scheduled_job('interval', hours=4)
def job_start_screener():
    start_screener()
    
@sched.scheduled_job('interval', hours=24)
def job_start_screener_all():
    start_screener_all()
    
@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes. หลอก heroku')
    


@app.route("/")
def home():
    return render_template('homepage.html')

@app.route("/start_screener")
def noti1():
    # res = start_screener()
    return render_template('asset.html')

@app.route("/result")
def result_page():
    # res = start_screener()
    return render_template('investResult.html')

@app.route("/start_screener/watch_list")
def noti1_1():
    res = start_screener()
    return res

@app.route("/start_screener_all")
def noti2():
    # res = start_screener_all()
    return render_template('buying.html')

@app.route("/start_screener_all/watch_list")
def noti2_2():
    if request.args.get('next_index'):
        next_index = request.args.get('next_index')
        res , current_index = start_screener_all(int(next_index))        
    return res


@app.route("/result_Performance")
def result():
    res = get_holding_performance()
    res = jsonify(res)
    return make_response(res)


if __name__ == '__main__':
    app.run(port=200,use_reloader=True,debug=True)
    
    # start_screener()
    # start_screener_all()
    # sched.start()
    