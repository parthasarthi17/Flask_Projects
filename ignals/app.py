from flask import Flask, request, render_template, redirect, jsonify, template_rendered, current_app
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, models_committed, before_models_committed
from flask_migrate import Migrate
#from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from blinker import Namespace


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
#login_manager = LoginManager()
#login_manager.init_app(app)
admin = Admin(app, name='Todo', template_mode='bootstrap3')

my_signals = Namespace()




app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///otbefgasuygvskydfgc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'some key'

#model_saved = my_signals.signal('model-saved')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    extra = db.Column(db.String(300), nullable=True)

    def __rep__(self):
        return '<Task %r>' % self.id

    @classmethod
    def signal_thing(sender, app, changes):
        print(sender)
        print(changes)
        print(changes[0][0])
        print(changes[0][1] )
        print('--------------------')
        if changes[0][0].content and changes[0][1]=='insert':
            print(changes[0][0].content)
            changes[0][0].extra = "okay"
        for model, change in changes:
            print('--------------------')
            print(model)
            if model == Todo:
                print("HELLO!")
            print(change)
            print('--------------------')

        print('hello - is this working?')








class MyModelView(ModelView):
    def is_accessible(self):
        return True

admin.add_view(MyModelView(Todo, db.session))



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
        db.session.add(new_task)
        before_models_committed.connect(Todo.signal_thing,  sender=app)

        db.session.commit()
        return redirect('/')

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
