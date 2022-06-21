from flask import Flask, request, render_template, redirect, jsonify, url_for
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from flask_caching import Cache


from random import randint
import base64

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='Todo', template_mode='bootstrap3')


app.config['CACHE_TYPE'] = "SimpleCache"
cache = Cache(app)


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/flasktest'
app.secret_key = 'some key'



########################################################################################################################

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
    checks = db.relationship('Check', backref='user', lazy=True)


    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

class Check(db.Model):
    __tablename__ = 'check'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_email = db.Column(db.String(25), db.ForeignKey('user.email'),
        nullable=False)

########################################################################################################################

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), nullable=False)
    data  = db.Column(db.LargeBinary )



########################################################################################################################
########################################################################################################################

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

########################################################################################################################
########################################################################################################################

class MyModelView(ModelView):
    def is_accessible(self):
        print(current_user)
        if current_user.is_authenticated:
            print(current_user.username)
            if current_user.username == 'admin':

                return True
            else:
                return False
        else:
            return False


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Todo, db.session))
admin.add_view(MyModelView(Check, db.session))
admin.add_view(MyModelView(Images, db.session))

########################################################################################################################
########################################################################################################################


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

x_args = reqparse.RequestParser()
x_args.add_argument("content", type=str, help = "dfsdf")

resource_fields = {
    'id' : fields.Integer,
    'content' : fields.String,
    'extra' : fields.String,
}


########################################################################################################################
########################################################################################################################


class UserList(Resource):

    @marshal_with(user_fields)
    @cache.cached(timeout = 300)
    def get(self):
        result = User.query.all()
        return result

    @marshal_with(user_fields)
    @cache.cached(timeout = 60)
    def post(self):
        args = u_args.parse_args()
        user = User(username=args['username'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()

        result = User.query.all()
        return result

api.add_resource(UserList, "/userlist")

########################################################################################################################
########################################################################################################################


class Login(Resource):
    @marshal_with(user_fields)
    def post(self):

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
                print(current_user.username)
                return result
            else:
                return 'Incorrect Password!'

        else:
            return 'The username does not exist!'

api.add_resource(Login, "/login")

class Logout(Resource):
    @marshal_with(user_fields)
    def post(self):
        print(current_user)
        result = current_user
        result.authenticated = False
        logout_user()
        db.session.commit()

        return jsonify({"message":"loggedout"})

api.add_resource(Logout, "/logout")

########################################################################################################################
########################################################################################################################


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


########################################################################################################################
########################################################################################################################


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

########################################################################################################################

@app.route('/loginadmin', methods=['GET'])
def loginadmin():
    result = User.query.filter_by(username='admin').first()
    login_user(result)
    return 'result'

@app.route('/logoutadmin', methods=['GET'])
def logoutadmin():
    logout_user()
    return 'result'

########################################################################################################################


@app.route('/random', methods=['GET'])
@cache.cached(timeout = 5)
def randomint():
    randnum = randint(0,500)
    return f'<h1>{randnum}</h1>'


########################################################################################################################

@app.route('/imagestab', methods=['GET', 'POST'])
def uploadimages():
    if request.method == 'POST':
        f = request.files['file']
        newimage = Images(file_name = f.filename, data = f.read())

        db.session.add(newimage)
        db.session.commit()
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        return redirect(url_for('download_file', name=f.filename))
    return render_template('image.html')

@app.route('/uploads/<name>')
def download_file(name):
    qimage = Images.query.filter_by(file_name=name).first()
    qimage = base64.b64encode(qimage.data).decode('ascii')

    return render_template("uploadedimage.html", qimage=qimage)


########################################################################################################################
########################################################################################################################


if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
