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


app = Flask(__name__)
CORS(app)


@app.route('/recognize', methods=['POST'])
def compareImage():
    data = request.get_json()
    encodedImage = data['imageEncoded']
    encoded_data = encodedImage.split(',')[1]
    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
    face_desc = get_face_embedding(imgRecovered)
    face_emb = vec2list(face_desc)
    retrieveResponse = retrieve(face_emb)
    print(retrieveResponse)
    response = app.response_class(
        response=json.dumps(retrieveResponse),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/user', methods=['POST'])
def insertUser():
    data = request.get_json()
    encodedImage = data['imageEncoded']
    name = data["name"]
    encoded_data = encodedImage.split(',')[1]
    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
    face_desc = get_face_embedding(imgRecovered)
    face_emb = vec2list(face_desc)
    update_table(1004, name, face_emb)
    response = app.response_class(
        response='Inserted successfully.',
        status=201,
        mimetype='application/json'
    )
    return response


@app.route('/')
def hello_world():
    return 'Hello, I am Flask in Docker!'
