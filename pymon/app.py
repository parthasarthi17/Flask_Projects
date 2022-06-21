from flask import Flask, render_template, request, url_for, redirect, jsonify, Response
from flask_pymongo import PyMongo
import pymongo
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from bson import json_util, ObjectId
import json

app = Flask(__name__)
api = Api(app)


try:
    mongo = pymongo.MongoClient(
    host= 'localhost',
    port = 27017,
    )
    mongo.server_info()
except:
    print('--------------failed to connect-------------------')

db = mongo.mydb1



u_args = reqparse.RequestParser()
u_args.add_argument ("firstname", type=str, help = "dfsdf")
u_args.add_argument ("lastname", type=str, help = "asd")
u_args.add_argument("new", type=str, help = 'sdfsf')
u_args.add_argument ("pets", type=str, help = "dfsdf", action='append')


page = {
     'firstname':fields.String,
     'lastname':fields.String,
     'object id': ObjectId()}


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

        return json.dumps(userlist, default=str)

pet_args = reqparse.RequestParser()
pet_args.add_argument ("pets", type=str, help = "dfsdf")


@app.route('/newuser', methods=['GET', 'POST'])
def userasd():
    if request.method == 'POST':
        args = u_args.parse_args()
        print('---______-__--__-___--_______---------__-_--_-_-_-__-__-__--_______-_--_--')
        user = {"firstname":args['firstname'], "lastname":args["lastname"], "Whatothersdon'thave":args["new"], "pets":args["pets"]}
        print(user)

        for x in ['pets']:
            print('----------___________________------------____________----------')
            print(x)


        print('-------------_________________________--------------------')

        db.users.insert_one(user)
        user["_id"]=str(user["_id"])

        #db.jobs.insert_one(job)

        return json.dumps(user)

@app.route('/user1', methods=['GET'])
def dasdasdasd():
    if request.method == 'GET':
        user = db.users.find_one({"firstname":"dsfkhgvj fsd"})
        print(user)
        print('---______-__--__-___--_______---------__-_--_-_-_-__-__-__--_______-_--_--')
        asdsadsadasd = list(db.users.find({"firstname":"fdsdsf"}))


        user["_id"]=str(user["_id"])

        job = {"title":"itufk,gjvfjgvj", "USER_ID": user['_id']}
        #db.jobs.insert_one(job)

        return json.dumps(user['pets'])



if __name__ =="__main__":
    app.run(debug=True)
