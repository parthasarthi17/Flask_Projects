 #! / usr / bin / env Python
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'



class Author(db.Model):
    name = db.Column(db.String(300),primary_key = True, unique=True, nullable=False)
#    article = db.relationship('Article', backref='author', uselist=False)

    def __rep__(self):
        return '<Writer: %r>' % self.name


@app.route('/authors/', methods=['POST','GET'])
def authors():
    if request.method == 'POST':
        author_name = request.form['author_name']
        new_author = Author(name=author_name)
        print(new_author.name)

        try:
            db.session.add(new_author)
            db.session.commit()
            return redirect('/authors/')
        except:
            return 'There was an error while adding the task'

    else:
        authorss = Author.query.all()
        return render_template("authors.html", authorss=authorss)


app.run(debug=True)
