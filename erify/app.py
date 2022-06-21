from flask import Flask, request, render_template, redirect, jsonify, render_template, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import simplejson as json
import jwt
from flask_marshmallow import Marshmallow
from functools import wraps

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
admin = Admin(app, name='Todo', template_mode='bootstrap3')
ma = Marshmallow(app)


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY']='sample'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///libraryverify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'asdasdasdasdasdasd1787@gmail.com'
app.config['MAIL_PASSWORD'] = 'Qwerty54321!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(15))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



class Tempuser(db.Model):
    __tablename__ = 'temp'

    tempemail = db.Column(db.String(25), primary_key=True)
    tempusername = db.Column(db.String(40), unique=True)
    temppassword = db.Column(db.String(15))


class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin.add_view(MyModelView(User, db.session))

def check_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.args.get('token')

        print("====================================",app.config["SECRET_KEY"])
        data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
        print(data)
        return func()
    return decorator


u_args = reqparse.RequestParser()
u_args.add_argument ("email", type=str, help = "dfsdf")
u_args.add_argument ("username", type=str, help = "asd")
u_args.add_argument ("password", type=str, help = "dfsasjdhasddf")
#u_args.add_argument ("authenticated", type=bool, help = "sdiohaf")

user_fields ={
    'email':fields.String,
    'username':fields.String,
    'password':fields.String,
    'authenticated':fields.Boolean,
}


t_args = reqparse.RequestParser()
t_args.add_argument ("tempemail", type=str, help = "dfsdf")
t_args.add_argument ("tempusername", type=str, help = "asd")
t_args.add_argument ("temppassword", type=str, help = "dfsasjdhasddf")
#u_args.add_argument ("authenticated", type=bool, help = "sdiohaf")

user_fields ={
    'tempemail':fields.String,
    'tempusername':fields.String,
    'temppassword':fields.String,
}



class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        result = User.query.all()
        return result
    @marshal_with(user_fields)
    def post(self):
        args = u_args.parse_args()
        user = User(username=args['username'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()

        result = User.query.all()
        return result
api.add_resource(UserList, "/userlist")



class Register(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = t_args.parse_args()
        test_email=args['tempemail']
        test_username=args['tempusername']
        test_password=args['temppassword']
        token = jwt.encode({ 'user' : test_username, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'],algorithm="HS256")

        print(token)
        send_token = token
        print(send_token)

        msg = Message(subject="Verification Mail", sender=app.config['MAIL_USERNAME'], recipients=['parthasarthi.aggarwal.ece20@itbhu.ac.in'])
        msg.html = render_template('/mails/resgistering.html', send_token = send_token, test_email = test_email, test_username = test_username, test_password=test_password  )
        mail.send(msg)

        return jsonify({"as":"mail sent!"})
api.add_resource(Register, "/register")

@app.route('/registering', methods=['GET','POST'])
@check_token
def authorised():
    print("=======================================================Inoked=======================================================")


    new_email = request.form['email']
    new_username = request.form['Username']
    new_pass = request.form['Pass_1']
    new_user = User(email=new_email, username=new_username, password=new_pass)
    db.session.add(new_user)
    db.session.commit()


    return 'ok'

if __name__ =="__main__":
    app.run(debug=True)
