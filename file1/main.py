from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swag/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db3232'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    extra = db.Column(db.String(300), nullable=True)

    def __rep__(self):
        return '<Task %r>' % self.id

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



@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)



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


class UserList(MethodResource, Resource):
    @doc(description='get user list.', tags=['UserListGetView'])
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
docs.register(UserList)


class Login(Resource):
    @marshal_with(user_fields)
    def post(self):

        if current_user.authenticated:
            print("okay!")

        else:
            args = u_args.parse_args()
            test_username=args['username']
            test_password=args['password']

            result = User.query.filter_by(username=test_username).first()

            if result:
                print('sdfsdf')

                if result.password == test_password:
                    print(result.email)
                    result.authenticated =True
                    db.session.commit()
                    print('asdsd')
                    login_user(result)
                    return jsonify({"status": "User logged in successfully"})
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
        logout_user(result)

api.add_resource(Logout, "/logout")


x_args = reqparse.RequestParser()
x_args.add_argument("content", type=str, help = "dfsdf")

resource_fields = {
    'id' : fields.Integer,
    'content' : fields.String,
    'extra' : fields.String,
}




class todotask(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        result = Todo.query.filter_by(id=task_id).first()
        if not result:
            print("doesn't exist")
        return result
api.add_resource(todotask, "/<int:task_id>")

class todotaskList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = Todo.query.all()
        return result
api.add_resource(todotaskList, "/todods")




@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        print(new_task.id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'

    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task)

if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
