from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def text(msg):
	print("HELLO!")
	send(msg, broadcast = True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	socketio.run(app, debug=True, port=8000)


#@socketio.on('message')
#def handle_json(json):
#	send(json, broadcast=True)
