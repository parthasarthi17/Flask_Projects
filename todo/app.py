from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
db = SQLAlchemy(app)
admin = Admin(app, name='todo', template_mode='bootstrap3')

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean' #optional_to_configure_swatch_theme
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

    def __rep__(self):
        return '<Task %r>' % self.id

admin.add_view(ModelView(Todo, db.session))


@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'

    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<str:content>')
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
