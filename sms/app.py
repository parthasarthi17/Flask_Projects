from flask import Flask, request, render_template, redirect, jsonify, url_for
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import vonage
import nexmo
import string
import random

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
admin = Admin(app, name='Todo', template_mode='bootstrap3')


VONAGE_API_KEY = '34c5914e'
VONAGE_API_SECRET = 'Sqhm2LBEuGFrXFlc'
VONAGE_NUMBER = '919667618874'

nexmo_client = nexmo.Client(
    key=VONAGE_API_KEY, secret=VONAGE_API_SECRET
)

app.config['SECRET_KEY'] = 'FLASK_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kuchbhi.db'




class someone(db.Model):
    __tablename__ = 'someone'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)


class Peeps(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    TempName = db.Column(db.String(40), unique=True)
    Unique = db.Column(db.String(40), unique=True)



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
            to_number = request.form['to_number']
            tempname = request.form['tempname']


            message = f'{id_generator()}'

            newpeep = Peeps(TempName = tempname, Unique = message)
            print(tempname)
            print(message)
            print(newpeep.TempName)
            print

            result = nexmo_client.send_message({
                'from': VONAGE_NUMBER,
                'to': to_number,
                'text': message,
            })

            db.session.add(newpeep)
            db.session.commit()

            print(result)

            return redirect(url_for('update', asd=tempname ))

    else:
        return render_template('index.html')

@app.route('/check/<string:asd>', methods=['GET','POST'])
def update(asd):

    print(asd)
    print('______________________________________________________________')
    checkuser = Peeps.query.filter_by(TempName=asd).first()
    print(checkuser.TempName)

    if request.method == 'POST':
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        checkuni = request.form['checkuni']
        if f'{checkuser.Unique}' == checkuni:

            newname = checkuser.TempName

            newuser = someone(username=newname)
            db.session.add(newuser)
            db.session.commit()
            print("_________-----------___________________------------------")



        return "NEW SOMEONE CREATED!"

    else:
        return render_template('check.html', checkuser=checkuser)




if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
