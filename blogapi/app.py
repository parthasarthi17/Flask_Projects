from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/asd'
app.secret_key = 'some key'


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(15))
    authenticated = db.Column(db.Boolean, default=False)
    preference = db.Column(db.String(40))

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

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True)
    body = db.Column(db.String(15))
    genre = db.Column(db.String(40))

    def __rep__(self):
        return '<Post %r>' % self.id


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

u_args = reqparse.RequestParser()
u_args.add_argument ("email", type=str, help = "dfsdf")
u_args.add_argument ("username", type=str, help = "asd")
u_args.add_argument ("password", type=str, help = "dfsasjdhasddf")
u_args.add_argument ("preference", type=str, help = "sda")

#u_args.add_argument ("authenticated", type=bool, help = "sdiohaf")
user_fields ={
    'email':fields.String,
    'username':fields.String,
    'password':fields.String,
    'authenticated':fields.Boolean,
    'preference':fields.String
}


post_args = reqparse.RequestParser()
post_args.add_argument("title", type=str, help = "sad")
post_args.add_argument("body", type=str, help = "dsa")
post_args.add_argument("genre", type=str, help = "das")
post_fields = {
    'id':fields.Integer,
    'title':fields.String,
    'body':fields.String,
    'genre':fields.String,
}



class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        result = User.query.all()
        return result
    @marshal_with(user_fields)
    def post(self):
        args = u_args.parse_args()
        user = User(username=args['username'], email=args['email'], password=args['password'], preference = args['preference'])
        db.session.add(user)
        db.session.commit()
        result = User.query.all()
        return result
api.add_resource(UserList, "/userlist")


class PostList(Resource):
    @marshal_with(post_fields)
    def get(self):
        if current_user.is_authenticated:
            if current_user.preference:
                pref = current_user.preference
                print(pref)
                result = Post.query.filter_by(genre=pref).all()
                return result
                print("---------xxxxokayxxxx---------!")
            else:
                result = Post.query.all()
                return result
        else:
            result = Post.query.all()
            return result
    @marshal_with(post_fields)
    def post(self):
        args= post_args.parse_args()
        post = Post(title = args['title'], body = args['body'], genre = args['genre'])
        db.session.add(post)
        db.session.commit()
        result = Post.query.all()
        return result
api.add_resource(PostList, "/posts")



class Login(Resource):
    @marshal_with(user_fields)
    def post(self):
        if current_user.is_authenticated:
            Print("ALREADY LOGGED IN!")
            return jsonify({"message":"please logout first!"})
        else:
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
                    return result
                else:
                    return 'Incorrect Password!'
            else:
                return 'The username does not exist!'
api.add_resource(Login, "/login")

class Logout(Resource):
    @marshal_with(user_fields)
    def post(self):

        result = current_user
        result.authenticated = False
        db.session.commit()
        z = current_user
        logout_user()
        return z
api.add_resource(Logout, "/logout")








if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
