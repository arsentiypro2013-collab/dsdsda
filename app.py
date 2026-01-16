import os
import eventlet
eventlet.monkey_patch()  # Обязательно первым!

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return jsonify({"status": "Сервер чата готов для SocketIO!"})

@socketio.on('connect')
def connect():
    emit('status', {'msg': 'Подключён'})

@socketio.on('message')
def handle_message(data):
    timestamp = datetime.now().strftime('%H:%M')
    msg = f"[{timestamp}] {data['name']}: {data['msg']}"
    emit('message', msg, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    emit('status', {'msg': 'Пользователь отключился'}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
