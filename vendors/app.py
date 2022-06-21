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

db = mongo.vendorsdb



u_args = reqparse.RequestParser()
u_args.add_argument ("Vendorname", type=str, help = "dfsdf")
u_args.add_argument ("service", type=str, help = "dfsdf")
u_args.add_argument ("description", type=str, help = "asd")
u_args.add_argument("subservices", type=dict, help = 'sdfsf', action='append')



@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':

        args = u_args.parse_args()
        vendor_name = args["Vendorname"]
        collection_name = db[vendor_name]


        print('-------------_________________________--------------------')
        Service = {"service":args['service'], "description":args['description'], "subservices":args["subservices"], }
        print('-------------_________________________--------------------')

        dbResponse = collection_name.insert_one(Service)
        print(dbResponse.inserted_id)

        return "Service added!"

    elif request.method == 'GET':
        serviceslist = list(db.vendor1.find())
        print('-------------------------')
        print(serviceslist)
        print('-------------------------')
        for u in serviceslist:
            u["_id"]=str(u["_id"])

        return json.dumps(serviceslist, default=str)


@app.route('/subs', methods=['GET'])
def subfilter():
    subserviceslist = list(db["vendor1"].find({"subservices":{'subservice' : ' type2'}}))
    print('-------------------------')
    print(subserviceslist)
    print('-------------------------')
    for u in subserviceslist:
        u["_id"]=str(u["_id"])

    return json.dumps(subserviceslist, default=str)


if __name__ =="__main__":
    app.run(debug=True)
