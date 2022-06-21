from flask import Flask, render_template, request, url_for, redirect, jsonify, Response
from flask_pymongo import PyMongo
import pymongo
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from bson import json_util, ObjectId
import json
from flask_caching import Cache


app = Flask(__name__)
api = Api(app)

app.config['CACHE_TYPE'] = "FileSystemCache"
app.config['CACHE_DIR'] = "/Users/parthasarthiaggarwal/desktop/sda/file"
app.config['CACHE_DEFAULT_TIMEOUT'] = 15

cache = Cache(app)



app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongodb_client = PyMongo(app)
db = mongodb_client.db

u_args = reqparse.RequestParser()
u_args.add_argument ("firstname", type=str, help = "dfsdf")
u_args.add_argument ("lastname", type=str, help = "asd")


@app.route('/', methods=['POST','GET'])
@cache.cached()
def home():
    if request.method == 'POST':
        args = u_args.parse_args()
        print('-------------_________________________--------------------')
        user = {"firstname":args['firstname'], "lastname":args["lastname"]}
        print('-------------_________________________--------------------')

        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)

        return "User added!"

    elif request.method == 'GET':
        userlist = list(db.users.find())
        print('-------------------------')
        print(userlist)
        print('-------------------------')
        for u in userlist:
            u["_id"]=str(u["_id"])

        return json.dumps(userlist)

@app.route('/user1', methods=['GET'])
def userasd():
    if request.method == 'GET':
        user = db.users.find_one({"firstname":"fdsdsf"})
        print(user)
        print('---______-__--__-___--_______---------__-_--_-_-_-__-__-__--_______-_--_--')
        asdsadsadasd = list(db.users.find({"firstname":"fdsdsf"}))
        print(asdsadsadasd)

        user["_id"]=str(user["_id"])

        job = {"title":"itufk,gjvfjgvj", "USER_ID": user['_id']}
        #db.jobs.insert_one(job)

        return json.dumps(user)




if __name__ =="__main__":
    app.run(debug=True)
