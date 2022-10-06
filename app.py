import cv2
from FaceEmbeddings import update_table
from FaceRecognitionFunctions import *
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json
from codecs import encode
from imageio import imread
import io
from createSQLfunctions import initDB
from routes import *


initDB()
app = Flask(__name__)
app.register_blueprint(routes)

CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, I am Flask in Docker!'
