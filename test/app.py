from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow


app = Flask(__name__)


db = SQLAlchemy(app)
ma = Marshmallow(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/dvdv'

#class Author(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(255))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "email", "_links")
    _links = ma.Hyperlinks({    "self": ma.URLFor("user_detail", values=dict(u_id="<id>")),    "list": ma.URLFor("users"),    })

user_schema = UserSchema()
users_schema = UserSchema(many=True)



@app.route('/create', methods=['POST'])
def addpost():
    email = request.json['email']
    password = request.json['password']

    new_user = User(email, password)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route("/api/users/")
def users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route("/api/users/<int:u_id>")
def user_detail(u_id):
    user = User.query.filter_by(id=u_id).first()
    return user_schema.dump(user)


#@app.route('/booklist', methods=['GET'])
#def booklist():
#    book_list = Book.query.all()
#    result = book_schemas.dump(book_list)
#    return jsonify(result)


@app.route('/helloworld', methods = ['GET'])
def helloworld():
    return jsonify({"hello":"world"})



if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
