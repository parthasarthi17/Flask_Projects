from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {}


def abort_if_todo_doesnt_exist(id):
    if id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, id):
        abort_if_todo_doesnt_exist(id)
        return TODOS[id]

    def delete(self, id):
        abort_if_todo_doesnt_exist(id)
        del TODOS[id]
        return '', 204

    def put(self, id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        id = int(max(TODOS.keys()).lstrip('todo')) + 1
        id = 'todo%i' % id
        TODOS[id] = {'task': args['task']}
        return TODOS[id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)
