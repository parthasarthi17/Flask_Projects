from flask import Flask, render_template, request, url_for, redirect, jsonify, Response
from flask_pymongo import PyMongo
import pymongo
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from bson import json_util, ObjectId
import json

app = Flask(__name__)
api = Api(app)

app.config["MONGO_URI"] = "mongodb+srv://parthasarthi:Parth12345@cluster0.nesrv.mongodb.net/mydb1?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = 'secret_key'
mongodb_client = PyMongo(app)
db = mongodb_client.db

u_args = reqparse.RequestParser()
u_args.add_argument ("firstname", type=str, help = "dfsdf")
u_args.add_argument ("lastname", type=str, help = "asd")


@app.route('/', methods=['POST','GET'])
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





if __name__ =="__main__":
    app.run(debug=True)
