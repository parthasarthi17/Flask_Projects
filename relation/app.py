from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with


app = Flask(__name__)

db = SQLAlchemy(app)
ma = Marshmallow(app)
admin = Admin(app, name='books', template_mode='bootstrap3')
migrate = Migrate(app, db)
api = Api(app)


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/testdb3'
app.secret_key = 'some key'

genres = db.Table('genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(25))
    #tags = db.relationship('Book', secondary=genres, backref='genres', lazy=True)
    def __init__(genre_name):
        self.genre_name = genre_name




class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    books = db.relationship('Book', backref='author', lazy=True)
    def __rep__(self):
        return '<Name %r>' % self.id


class Sequel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proptitle = db.Column(db.String(25))
    books = db.relationship('Book', backref='sequel', uselist=False, lazy=True)
    def __rep__(self):
        return '<proptitle %r>' % self.id


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), unique=True)
    description = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    sequel_id = db.Column(db.Integer, db.ForeignKey('sequel.id'))
    genre_id = db.relationship('Genre', secondary=genres, backref='book', lazy=True)


    def __init__(self, title, description, author, sequel):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.sequel_id = sequel_id
        sef.genre_id = genre_id




admin.add_view(ModelView(Author, db.session))
admin.add_view(ModelView(Sequel, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Genre, db.session))



genre_fields = {
    'id':fields.Integer,
    'genre_name':fields.String,
}

author_fields= {
    'id':fields.Integer,
    'name':fields.String,
}


sequel_fields= {
    'id':fields.Integer,
    'proptitle':fields.String,
}


book_fields = {
    'id':fields.Integer,
    'title':fields.String,
    'description':fields.String,
    'author_id':fields.Integer,
    'sequel_id':fields.Integer,
    'genre_id':fields.Nested(genre_fields),
}

class BookList(Resource):
    @marshal_with(book_fields)
    def get(self):
        result = Book.query.all()
        return result
api.add_resource(BookList, "/booklist")

class genrelist(Resource):
    @marshal_with(genre_fields)
    def get(self, book_id):
        data = Book.query.filter_by(id = book_id).first()
        dataset = data.genre_id
        return dataset
api.add_resource(genrelist, "/genrelist/<int:book_id>")






if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
