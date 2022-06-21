from flask import Flask, render_template, request, url_for, redirect, jsonify, Response
from flask_pymongo import PyMongo
import pymongo
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from bson import json_util, ObjectId
import json

app = Flask(__name__)
api = Api(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/kjbsdasdas"
app.config['SECRET_KEY'] = 'ajkhsdvads'
mongodb_client = PyMongo(app)
db = mongodb_client.db


reply_fields = {
    'id':fields.Integer,
    'depth':fields.Integer,
    'contt':fields.String,
    'post_id':fields.Integer,
    'parent_id':fields.Integer,
}


comments_fields = {
    'id':fields.Integer,
    'depth':fields.Integer,
    'contt':fields.String,
    'post_id':fields.Integer,
    'parent_id':fields.Integer,
    'parent':fields.Nested(reply_fields),
    'replies':fields.Nested(reply_fields),
}



@app.route('/', methods=['POST','GET'])
def home():

    print('-------------_________________________--------------------')
    result = db.posts.find_one({"_id":"POST1"})
    print(result)
    print('-------------_________________________--------------------')

    #xxx = db.posts.insert_one({"_id":"comment2" , "contt":"sdfsdffsd.", "parent": "POST1" })
    #db.categories.find( { parent: "Databases" } )
    xyz = list(db.posts.find( { "parent": "POST1" } ))

    print(xyz)




    return json.dumps(xyz, default=str)


if __name__ =="__main__":
    app.run(debug=True)
