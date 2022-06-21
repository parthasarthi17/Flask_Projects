from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from app.models.models import Todo
from app import app, db, api

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
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

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
