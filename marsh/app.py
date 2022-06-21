from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow


app = Flask(__name__)


db = SQLAlchemy(app)
ma = Marshmallow(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasktest.db'

#class Author(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), unique=True)
    description = db.Column(db.String(255))
    author = db.Column(db.String(25))

    def __init__(self, title, description, author):
        self.title = title
        self.description = description
        self.author = author


class BookSchema(ma.Schema):
    class Meta:
        fields = ("title", "description", "author")

book_schema = BookSchema()
book_schemas = BookSchema(many=True)



@app.route('/post', methods=['POST'])
def addpost():
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']

    new_book = Book(title, description, author)
    db.session.add(new_book)
    db.session.commit()

#    return jsonify(title = new_book.title, id = new_book.id, description = new_book.description, author = new_book.author)
    return book_schema.jsonify(new_book)



@app.route('/booklist', methods=['GET'])
def booklist():
    book_list = Book.query.all()
    result = book_schemas.dump(book_list)
    return jsonify(result)


@app.route('/helloworld', methods = ['GET'])
def helloworld():
    return jsonify({"hello":"world"})



if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
