from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random, time, threading

import utils.monitor as m
import utils.encoder as e

app = Flask(__name__)
socketio = SocketIO(app)


def send_data():
    while True:
        data = {
            'values': m.data_dump, 
            "image" : e.encode(m.latest_frame)
            }
        #print(data)
        socketio.emit('update', data)
        time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set_light', methods=['POST'])
def set_light():
    return {"status": "ok", "value": m.toggle_light()}



if __name__ == '__main__':
    # Start your background threads
    threading.Thread(target=m.main, daemon=True).start()
    threading.Thread(target=send_data, daemon=True).start()

    # Only run one server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)