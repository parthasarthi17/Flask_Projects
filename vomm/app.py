from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
admin = Admin(app, name='Todo', template_mode='bootstrap3')


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gfdgdf.db'
app.secret_key = 'some key'

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True)
    content = db.Column(db.String(300), nullable=False)
    commnt = db.relationship('Comments', backref='Post')

    def __rep__(self):
        return '<Task %r>' % self.id

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    depth = db.Column(db.Integer)
    contt = db.Column(db.String(300), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    replies = db.relationship('Comments', backref=db.backref('parent', remote_side=[id]), lazy='select')
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)




class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Comments, db.session))

reply_fields = {
    'id':fields.Integer,
    'depth':fields.Integer,
    'contt':fields.String,
    'post_id':fields.Integer,
    'parent_id':fields.Integer,
}


comments_fields = {
    'id':fields.Integer,
    'depth':fields.Integer,
    'contt':fields.String,
    'post_id':fields.Integer,
    'parent_id':fields.Integer,
    'parent':fields.Nested(reply_fields),
    'replies':fields.Nested(reply_fields),
}

class CommentsList(Resource):
    @marshal_with(comments_fields)
    def get(self):
        result = Comments.query.all()
        print('______________________----------------------')
        print('______________________----------------------')
        return result
api.add_resource(CommentsList, "/")


x_args = reqparse.RequestParser()
x_args.add_argument("contt", type=str, help = "dfsdf")

class AddComment(Resource):
    @marshal_with(comments_fields)
    def post(self, comm_id):
        args= x_args.parse_args()
        newcommnt = Comments(contt = args['contt'])

        parentcomment = Comments.query.filter_by(id = comm_id).first()

        newcommnt.parent_id = comm_id
        newcommnt.depth = parentcomment.depth+1
        newcommnt.post_id = parentcomment.post_id

        db.session.add(newcommnt)
        db.session.commit()

        result = newcommnt

        return result

api.add_resource(AddComment, "/replyto/<int:comm_id>")


@app.route("/post/<int:post_id>", methods=['POST','GET'])
def post(post_id):

    post = Post.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(post_id = post_id, depth=0).all()
    allcomments = Comments.query.filter_by(post_id = post_id).all()

    return render_template('posts.html', post=post, comments=comments, allcomments=allcomments)


if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
