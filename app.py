from flask import Flask, render_template, session
from flask_socketio import SocketIO, join_room, leave_room, emit, disconnect
from flask_session import Session
from threading import Lock

import json

async_mode = None 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sbx91310'
app.config['SESSION_TYPE'] = 'filesystem'
sourceURL = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4'
Session(app)
socketio = SocketIO(app, async_mode=async_mode, manage_session=False)
thread = None
thread_lock = Lock()

messages = []


@app.route('/')
def index():
  return render_template('index.html',
                          sync_mode=socketio.async_mode,
                          url=sourceURL)

@socketio.on('connect', namespace='/chat')
def create_connection():
  if session.get('username') is None:
    username = "null"
  else:
    username = session.get('username')
  
  emit('create_connection', {'username': username})

@socketio.on('join', namespace='/chat')
def join_chat(data):
  session['username'] = data['username']
  username = data['username']
  room = data['room']
  join_room(room)

@socketio.on('broadcast', namespace='/chat')
def broadcast_msg(message):
    emit('send_broadcast',
          {'data': message['data']}, room='chat')
    messages.append(message['data'])
    print(message['data'])

@socketio.on('send_msg', namespace='/chat')
def chat_message(message):
    username = session['username']
    emit('post_msg',
         {'username': username,'message': message['data']}, room='chat')
    print_msg = f"{username}: {message['data']}"
    messages.append(print_msg)
    print(print_msg)


@socketio.on('load_chat_history', namespace='/chat')
def display_msg():
    print("loading chat history")



if __name__ == '__main__':
  socketio.run(app, debug=False)
                          