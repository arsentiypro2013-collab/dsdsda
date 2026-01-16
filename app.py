from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat_key!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return jsonify({"status": "Чат-сервер готов! Подключайтесь SocketIO."})

@socketio.on('connect')
def connect():
    emit('status', {'msg': 'Подключён к чату'})

@socketio.on('message')
def handle_message(data):
    timestamp = datetime.now().strftime('%H:%M')
    name = data.get('name', 'Anon')
    msg = f"[{timestamp}] {name}: {data['msg']}"
    emit('message', msg, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    emit('status', {'msg': 'Пользователь вышел'}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
