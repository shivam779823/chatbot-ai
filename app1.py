from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('app.html')

@socketio.on('message')
def handle_message(msg):
    print('Message received:', msg)
    socketio.emit('response', 'Message received by App 1: ' + msg)

if __name__ == '__main__':
    socketio.run(app, debug=True)
