from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
admin = Admin(app, name='Todo', template_mode='bootstrap3')


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sometinhgagsadasdasdavhkvavLTRWYSUTCK.db'
app.secret_key = 'some key'



class CostCenter(db.Model):
     __tablename__ = 'costcenter'
     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     name = db.Column(db.String)
     number = db.Column(db.Integer)

class Expense(db.Model):

    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    costcenter_id = db.Column(db.Integer, db.ForeignKey('costcenter.id'))
    costcenter = db.relationship('CostCenter')
    value = db.Column(db.Float)
    date = db.Column(db.Date)



admin.add_view(ModelView(CostCenter, db.session))
admin.add_view(ModelView(Expense, db.session))



@app.route('/', methods=['POST','GET'])
def home():
    sumofids = db.session.query(func.count(Todo.id).filter(Todo.content))
    print('__________________________________________________')
    print(sumofids)
    print('--------------------------------------------------')
    return Hello


if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
