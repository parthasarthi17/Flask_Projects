from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_pymongo import PyMongo
import pymongo
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from bson import json_util, ObjectId
import json


#from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

import time

app = Flask(__name__)
api = Api(app)
#scheduler = APScheduler()
#scheduler.init_app(app)
#scheduler.start()



try:
    mongo = pymongo.MongoClient(
    host= 'localhost',
    port = 27017,
    )
    mongo.server_info()
except:
    print('--------------failed to connect-------------------')

db = mongo["crondb"]
app.secret_key = 'some key'

#number = {"_id":"Number", "value":1}
#db.int.insert_one(number)

#def scheduled_task(task_id):
#    for i in range(10):
#        time.sleep(1)
#        print('Task {} running iteration {}'.format(task_id, i))





def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def incrementing():
    number = db.int.find_one({"_id":"Number"})
    x = number["value"] + 1
    print(number["value"])

    db.int.update_one({"_id":"Number"}, {"$set":{"value":x}})

def returning():
    print("Hello!")

def job_function():
    print("Hello World")


@app.route('/')
def index():
    x = scheduler.add_job(func=returning, trigger="interval", seconds=5)
    return "x"


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=15)
scheduler.add_job(func=incrementing, trigger="interval", seconds=5)
scheduler.add_job(job_function, 'cron', month='8-12', day='2nd fri', hour='0-4')

scheduler.start()

##Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())










if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
