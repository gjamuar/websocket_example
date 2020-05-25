from random import random

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from flask_cors import CORS, cross_origin
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()

import random

from RecognizerService import RecognizerService
from config import DatabasePath, mode, FingerprintDirectory, RecordingTime
import json

recognizer = RecognizerService(DatabasePath)


def recognize(currentSocketId, file_name):
    # match_list = recognizer.stream_recognize_file_path("mp3/Brad-Sucks--Total-Breakdown.mp3")
    match_list = recognizer.stream_recognize_file_path("uploads/"+file_name)
    for match in match_list:
        y = json.dumps(match)
        print(str(currentSocketId) + ':' + y)
        socketio.emit('newnumber', y, room=currentSocketId)
        socketio.sleep(0.0001)


def randomNumberGenerator(currentSocketId):
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    # infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = round(random() * 10, 3)
        print(str(currentSocketId) + ':' + str(number))
        # socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.emit('newnumber', {'number': number}, room=currentSocketId)
        socketio.sleep(0.001)


# @app.route('/')
# def index():
#     # only by sending this page first will the client be connected to the socketio instance
#     return render_template('index.html')

# @cross_origin()
@socketio.on('connect', namespace='/test1')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)


# @cross_origin()
# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@socketio.on('test')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    print('received json: ' + str(json['audiofile']))
    audio_file = json['audiofile']
    emit('my response', json)
    # global thread
    print('Client connected')
    # print(json['audiofile'])
    # if json.filename == '':
    #     resp = jsonify({'message': 'No file selected for uploading'})
    #     resp.status_code = 400
    #     return resp
    # if json and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Start the random number generator thread only if the thread has not been started before.
    # if not thread.isAlive():
    #     print("Starting Thread")
    #     thread = socketio.start_background_task(randomNumberGenerator)

    currentSocketId = request.sid
    print("Starting Thread for ID: " + currentSocketId)
    # socketio.start_background_task(randomNumberGenerator, currentSocketId)
    socketio.start_background_task(recognize, currentSocketId, audio_file)


if __name__ == '__main__':
    # CORS(app, origins='*')
    socketio.run(app, host='0.0.0.0', port=5002)
