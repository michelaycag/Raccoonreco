from socket import timeout
import psycopg2
import cv2
import dlib
from psycopg2.extras import execute_values
import os
from FaceEmbeddings import cam_execMike, update_table
from FaceRecognitionFunctions import *
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json
from codecs import encode
import numpy as np
from imageio import imread
import io


app = Flask(__name__)
CORS(app)

# name = "Harbhajan_Singh"
# img = dlib.load_rgb_image(work_dir + name + '/' + name + '_0001.jpg')
#img = dlib.load_rgb_image("./tmp/boneta.jpg")
#face_desc = get_face_embedding(img)
#face_emb = vec2list(face_desc)


@app.route('/recognize', methods=['POST'])
def compareImage():
    data = request.get_json()
    encodedImage = data['imageEncoded']
    encoded_data = encodedImage.split(',')[1]
#   decoded_data = base64.b64decode(encoded_data)
    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
#   np_data = np.fromstring(decoded_data,np.uint8)
#   imgRecovered = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
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
#   decoded_data = base64.b64decode(encoded_data)
    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
#   np_data = np.fromstring(decoded_data,np.uint8)
#   imgRecovered = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    face_desc = get_face_embedding(imgRecovered)
    face_emb = vec2list(face_desc)
    update_table(1004, name, face_emb)
    response = app.response_class(
        response='Inserted successfully.',
        status=201,
        mimetype='application/json'
    )
    return response

# retrieve busca la string de cosos en la base de datos
# print(retrieve(face_emb))
# cam_execMike()
