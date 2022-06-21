from app import app

#x_args = reqparse.RequestParser()
#x_args.add_argument("content", type=str, help = "dfsdf")

#resource_fields = {
#    'id' : fields.Integer,
#    'content' : fields.String,
#    'extra' : fields.String,
#}


#class todotask(Resource):
#    @marshal_with(resource_fields)
#    def get(self, task_id):
#        result = Todo.query.filter_by(id=task_id).first()
#        if not result:
#            print("doesn't exist")
#        return result
#api.add_resource(todotask, "/<int:task_id>")

#class todotaskList(Resource):
#    @marshal_with(resource_fields)
#    def get(self):
#        result = Todo.query.all()
#        return result
#api.add_resource(todotaskList, "/todods")



if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
