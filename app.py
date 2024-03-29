from flask import Flask
from flask_cors import CORS


UPLOAD_FOLDER = 'uploads'
FINGERPRINT_FOLDER = 'mp3'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FINGERPRINT_FOLDER'] = FINGERPRINT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
cors = CORS(app)