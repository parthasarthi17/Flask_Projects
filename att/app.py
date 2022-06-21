from flask import Flask, request, render_template, redirect, jsonify, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import date, datetime
from flask_mail import Mail, Message
import simplejson as json
from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='Todo', template_mode='bootstrap3')
ma = Marshmallow(app)


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/attendance'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'asdasdasdasdasdasd1787@gmail.com'
app.config['MAIL_PASSWORD'] = 'Qwerty54321!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = 'some key'

mail = Mail(app)


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(15))
    authenticated = db.Column(db.Boolean, default=False)
    checks = db.relationship('Check', backref='user', lazy=True)

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

class Check(db.Model):
    __tablename__ = 'check'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120), nullable=False)
    timing = db.Column(db.String(120), nullable=False)
    person_email = db.Column(db.String(25), db.ForeignKey('user.email'),
        nullable=False)
    def __rep__(self):
        return '<Check %r>' % self.id



@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Check, db.session))



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



class CheckIn(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = u_args.parse_args()
        test_username=args['username']
        test_password=args['password']
        result = User.query.filter_by(username=test_username).first()
        if result:
            print('_________________________________________________')
            if result.password == test_password:
                print(result.email)
                result.authenticated =True
                db.session.commit()
                print('--------------------------------------------------')
                login_user(result)
                if current_user.is_authenticated:
                    print(f'{current_user.username}')


                    subj = f'CHECK IN TIME - {current_user.username}'
                    bod = f'{current_user.username} checked in on {date.today()}, at {datetime.now()}'

                    print(subj)
                    print(bod)
                    msg = Message(subject=subj, sender=app.config['MAIL_USERNAME'], recipients=['parthasarthi.aggarwal.ece20@itbhu.ac.in'])
                    msg.html = render_template('/mails/checkin.html', user=current_user, today = date.today(), now =datetime.now() )


                    newcheckin = Check(type = "CHECK_IN", timing =[datetime.now()], person_email=[current_user.email])
                    db.session.add(newcheckin)
                    db.session.commit()

                    mail.send(msg)
                    result.authenticated =False
                    db.session.commit()
                    logout_user()

                    return jsonify({"as":"mail sent!"})
                else:
                    return jsonify({"message":"error while logging in!"})
                return result
            else:
                return 'Incorrect Password!'
        else:
            return 'The username does not exist!'
api.add_resource(CheckIn, "/checkin")




class CheckOUT(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = u_args.parse_args()
        test_username=args['username']
        test_password=args['password']
        result = User.query.filter_by(username=test_username).first()
        if result:
            print('_________________________________________________')
            if result.password == test_password:
                print(result.email)
                result.authenticated =True
                db.session.commit()
                print('--------------------------------------------------')
                login_user(result)
                if current_user.is_authenticated:
                    print(f'{current_user.username}')


                    subj = f'CHECK OUT TIME - {current_user.username}'
                    bod = f'{current_user.username} checked out on {date.today()}, at {datetime.now()}'

                    print(subj)
                    print(bod)

                    msg = Message(subject=subj, sender=app.config['MAIL_USERNAME'], recipients=['parthasarthi.aggarwal.ece20@itbhu.ac.in'])
                    msg.html = render_template('/mails/checkout.html', user=current_user, today = date.today(), now =datetime.now() )

                    newcheckout = Check(type = "CHECK_OUT", timing =[datetime.now()], person_email=[current_user.email])
                    db.session.add(newcheckout)
                    db.session.commit()

                    mail.send(msg)
                    result.authenticated =False
                    logout_user()
                    db.session.commit()

                    return jsonify({"as":"mail sent!"})
                else:
                    return jsonify({"message":"error while logging in!"})
                return result
            else:
                return 'Incorrect Password!'
        else:
            return 'The username does not exist!'
api.add_resource(CheckOUT, "/checkout")



class CheckSchema(ma.Schema):
    class Meta:
        fields = ("type", "timing", "person_email")

check_schema = CheckSchema()
check_schemas = CheckSchema(many=True)


@app.route('/user/<string:email_id>', methods=['GET'])
def chcecks(email_id):
    data = User.query.filter_by(email = email_id).first()
    dataset = data.checks
    result = check_schemas.dump(dataset)
    return jsonify(result)

@app.route('/user/<string:email_id>/checkin', methods=['GET'])
def checkslogin(email_id):
    data = Check.query.filter_by(person_email = email_id, type ="CHECK_IN").all()
    result = check_schemas.dump(data)
    return jsonify(result)

@app.route('/user/<string:email_id>/checkout', methods=['GET'])
def checkslogout(email_id):
    data = Check.query.filter_by(person_email = email_id, type ="CHECK_OUT").all()
    result = check_schemas.dump(data)
    return jsonify(result)


@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'POST':
        print(request.form)
        emailid=request.form['emailid']
        body=request.form['body']
        subject=request.form['subject']

        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[emailid])
        msg.body = body
        mail.send(msg)
        return redirect('/')

    else:
        return render_template("index.html")




if __name__ =="__main__":
    app.run(debug=True)
