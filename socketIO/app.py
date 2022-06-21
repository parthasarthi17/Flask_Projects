from flask import Flask, request, render_template, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_session import Session

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='Todo', template_mode='bootstrap3')

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tesads.db'
app.secret_key = 'some key'

Session(app)
socketio = SocketIO(app, manage_session=False)


@socketio.on('message')
def handle_message(data):
    print('---------------------------------------------------------------------')
    print('received message: ' + data)
    print('---------------------------------------------------------------------')
    send(msg, broadcast=True)
    


if __name__ == '__main__':
    socketio.run(app)
