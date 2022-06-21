from flask import Flask, request, jsonify, make_response, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY']='sample'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///library3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

def check_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.args.get('token')

        print("====================================",app.config["SECRET_KEY"])
        data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
        print(data)
        return func()
    return decorator



@app.route('/')
def index():
    return render_template('login.html')


@app.route('/auth')
@check_token
def authorised():
    print("=======================================================Inoked")
    return 'ok'
#in url type: "http://127.0.0.1:5000/auth?token=GENERATED_TOKEN"

@app.route('/login', methods = ['POST'])
def login():
    if request.form['username'] and request.form['password'] == 'password':
        token = jwt.encode({ 'user' : request.form['username'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'],algorithm="HS256")
        return jsonify({'token' : token})
#generates token

if  __name__ == '__main__':
     app.run(debug=True)
