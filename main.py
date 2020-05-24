import os
# import urllib.request

from RecognizerService import RecognizerService
from app import app
from flask import Flask, request, redirect, jsonify,Response
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from config import DatabasePath, mode, FingerprintDirectory, RecordingTime


ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav'])

recognizer = RecognizerService(DatabasePath)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@cross_origin()
@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # result = recognizer.recognize(filename)
        # resp = jsonify(result)
        resp = jsonify(filename)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@cross_origin()
@app.route('/file-upload-stream', methods=['POST'])
def upload_file_stream():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return Response(recognizer.recognize_stream(filename))
        # resp = jsonify(result)
        # resp.status_code = 200
        # return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@cross_origin()
@app.route('/fingerprint', methods=['POST'])
def fingerprint_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename_path = os.path.join(app.config['FINGERPRINT_FOLDER'], filename)
        file.save(filename_path)
        result = recognizer.finger_print(filename_path)
        resp = jsonify(result)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


if __name__ == "__main__":
    CORS(app, origins='*')
    app.run(port=5001)
