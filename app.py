from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time, threading

import utils.monitor as m
import utils.encoder as e

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def send_data():
    while True:
        if m.heartbeat_active:
            data = m.data_dump
            socketio.emit('update', data)
        time.sleep(2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set_light/<serial>', methods=['POST'])
def set_light(serial):
    return {"status": "ok", "value": m.toggle_light(serial)}


@socketio.on('command')
def handle_command(data):
    return {"status": "ok", "value": m.handle_command(data)}


if __name__ == '__main__':
    # Start your background threads
    threading.Thread(target=m.main, daemon=True).start()
    threading.Thread(target=send_data, daemon=True).start()

    # Only run one server
    socketio.run(app, host='0.0.0.0', port=5001, debug=False)