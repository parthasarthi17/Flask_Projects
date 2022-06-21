from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='Todo', template_mode='bootstrap3')


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///libraryld.db'
app.secret_key = 'some key'



class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')


    def __rep__(self):
        return '<Task %r>' % self.id

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25))
    username = db.Column(db.String(40))
    password = db.Column(db.String(15))
    authenticated = db.Column(db.Boolean, default=False)
    liked_posts = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    def get_id(self):
        return self.username
    def is_authenticated(self):
        return self.authenticated
    def is_anonymous(self):
        return False

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id,PostLike.post_id == post.id).count() > 0




@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class MyModelView(ModelView):
    def is_accessible(self):
        return True

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))



u_args = reqparse.RequestParser()
u_args.add_argument ("email", type=str, help = "dfsdf")
u_args.add_argument ("username", type=str, help = "asd")
u_args.add_argument ("password", type=str, help = "dfsasjdhasddf")

user_fields ={
    'email':fields.String,
    'username':fields.String,
    'password':fields.String,
    'authenticated':fields.Boolean,
}



@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)



if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
