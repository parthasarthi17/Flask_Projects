from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    extra = db.Column(db.String(300), nullable=True)

    def __rep__(self):
        return '<Task %r>' % self.id


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(15))
    authenticated = db.Column(db.Boolean, default=False)

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
