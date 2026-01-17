import os
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit

# Папка для файлов
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat_key!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socketio = SocketIO(app, cors_allowed_origins="*")  # без async_mode, auto threading

# --- HTTP ---

@app.route('/')
def index():
    return jsonify({"status": "Чат-сервер готов! Подключайтесь по SocketIO."})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    name = request.form.get('name', 'Anon')
    if not file:
        return jsonify({'error': 'no file'}), 400

    filename = file.filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    file_url = f"/files/{filename}"
    timestamp = datetime.now().strftime("%H:%M")
    msg = f"[{timestamp}] {name} отправил файл: {filename} ({file_url})"
    socketio.emit('message', msg, broadcast=True)
    return jsonify({'status': 'ok', 'url': file_url})

@app.route('/files/<path:filename>')
def files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# --- SocketIO events ---

@socketio.on('connect')
def connect():
    emit('status', {'msg': 'Пользователь подключился к чату'}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    timestamp = datetime.now().strftime('%H:%M')
    name = data.get('name', 'Anon')
    text = data.get('msg', '')
    msg = f"[{timestamp}] {name}: {text}"
    emit('message', msg, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    emit('status', {'msg': 'Пользователь отключился'}, broadcast=True)

if __name__ == '__main__':
    # Для Render — allow_unsafe_werkzeug=True
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
