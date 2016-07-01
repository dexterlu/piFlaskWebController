from gevent import monkey
monkey.patch_all()

import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.socketio import SocketIO

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

pin_out_1 = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_out_1, GPIO.OUT)
GPIO.output(pin_out_1, True)

@app.route('/')
def main():
    return render_template('main.html')

@socketio.on('connect', namespace='/socket')
def ws_conn():
    data = {
        'button_1': GPIO.input(pin_out_1)
    }
    socketio.emit('status_btn', data, namespace='/socket')

@socketio.on('button', namespace='/socket')
def ws_btn(message):
    button = message.get('button')
    if button==1:
        GPIO.output(pin_out_1, not GPIO.input(pin_out_1))
        data = {
            'button_1': GPIO.input(pin_out_1)
        }
        socketio.emit('status_btn', data, namespace='/socket')

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5008)