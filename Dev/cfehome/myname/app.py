from flask import Flask, request, render_template, redirect, jsonify, session, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
socketio=SocketIO(app)

app.secret_key = 'not so secret'
app.debug = True






@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.' + '-' + f'({datetime.now()})' }, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg'] + '-' + f'({datetime.now()})'}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.' + '-' + f'({datetime.now()})'}, room=room)








@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['room'] = request.form['room']
        return redirect('/chat')
    return render_template('index.html')


@app.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect('/')
    return render_template('chat.html', name=name, room=room)




if __name__ =="__main__":
#    app.run(debug=True, host='localhost', port=8000)
     socketio.run(app)
