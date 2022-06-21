from app import db

class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(15))
    authenticated = db.Column(db.Boolean, default=False)
    preference = db.Column(db.String(40))

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True)
    body = db.Column(db.String(15))
    genre = db.Column(db.String(40))

    def __rep__(self):
        return '<Post %r>' % self.id
