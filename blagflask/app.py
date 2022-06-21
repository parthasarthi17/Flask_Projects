 #! / usr / bin / env Python
from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from datetime import date, datetime
from sqlalchemy import desc, nulls_first, nullslast, asc



app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
admin = Admin(app, name='blog', template_mode='bootstrap3')

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/blogtest'
app.secret_key = 'some key'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    article = db.relationship('Article', backref='writer', lazy=True)

#    article = db.relationship('Article', backref='author', lazy=True)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    writer_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    datecreated = db.Column(db.String(120), nullable=True)
    commnt = db.relationship('Comments', backref='Post')

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    depth = db.Column(db.Integer)
    contt = db.Column(db.String(300), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    replies = db.relationship('Comments', backref=db.backref('parent', remote_side=[id]), lazy='select')
    datecommented = db.Column(db.String(120), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)


class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin.add_view(MyModelView(Author, db.session))
admin.add_view(MyModelView(Article, db.session))
admin.add_view(MyModelView(Comments, db.session))



@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        author_name = request.form['author_name']
        new_author = Author(name=author_name)
        #print(new_author.name)

        db.session.add(new_author)
        db.session.commit()
        return redirect('/')

    else:
        authorss = Author.query.all()
        return render_template("authors.html", authorss=authorss)

@app.route('/posts', methods=['POST','GET'])
def postlist():
    authorss = Author.query.all()
    postlist = Article.query.order_by(asc(Article.datecreated)).all()
    return render_template("articlelist.html", authorss=authorss, postlist = postlist)


@app.route("/post/<int:post_id>", methods=['POST','GET'])
def post(post_id):
    post = Article.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(post_id = post_id, depth=0).all()
    allcomments = Comments.query.filter_by(post_id = post_id).all()
    writer = Author.query.filter_by(id = post.writer_id).first()
    print(post.writer_id)
    print(writer.name)

    return render_template('posts.html', post=post, comments=comments, allcomments=allcomments, writer=writer)


@app.route("/replyto/<int:comm_id>", methods=['POST','GET'])
def replying(comm_id):
    parent_commnt = Comments.query.filter_by(id = comm_id).first()
    if request.method == 'POST':
        comment_content = request.form['content']
        newcommnt = Comments(contt=comment_content)
        newcommnt.parent_id = comm_id
        newcommnt.depth = parent_commnt.depth+1
        newcommnt.post_id = parent_commnt.post_id
        newcommnt.datecommented = datetime.now()

        db.session.add(newcommnt)
        db.session.commit()

        return redirect(f'/post/{parent_commnt.post_id}')


    return render_template("replying.html", parent_commnt=parent_commnt)

@app.route("/commenton/<int:postid>", methods=['POST','GET'])
def commenting(postid):
    posts = Article.query.filter_by(id = postid).first()
    if request.method == 'POST':
        comment_content = request.form['content']
        print('-----------------------------------------------')

        print(posts.id)

        newcommnt = Comments(contt=comment_content)
        newcommnt.depth = 0
        newcommnt.datecommented = datetime.now()
        newcommnt.post_id = postid


        db.session.add(newcommnt)
        db.session.commit()

        return redirect(f'/post/{postid}')


    return render_template("commenting.html", posts=posts)





@app.route('/asd', methods=['POST','GET'])
def articlelist():
    if request.method == 'POST':
        print(request.form)
        article_title = request.form['article_title']
        article_description = request.form['article_description']
        article_writer = request.form['article_writer']
        print(article_writer)

        new_article = Article(title=article_title,description=article_description,writer_id=article_writer)
        new_article.datecreated = datetime.now()
        #print(new_author.name)

        db.session.add(new_article)
        db.session.commit()
        return redirect('/asd')

    else:
        dataset = Author.query.all()
        articless = Article.query.all()
        return render_template("addarticles.html", articless=articless, dataset=dataset)



if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
