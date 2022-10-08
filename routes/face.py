import cv2
from FaceEmbeddings import update_table
from FaceRecognitionFunctions import *
from flask import request,  Response, stream_with_context
import base64
import json
from imageio import imread
import io
from . import routes

@routes.route('/face', methods=['PUT'])
def compareImage():
    data = request.get_json()
    encodedImage = data['imageEncoded']
    encoded_data = encodedImage.split(',')[1]
    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
    face_desc = get_face_embedding(imgRecovered)
    face_emb = vec2list(face_desc)
    retrieveResponse = retrieve(face_emb)
    response = Response(stream_with_context(json.dumps(retrieveResponse)), mimetype='application/json')
    return response


@routes.route('/face', methods=['POST'])
def insertFace():
    data = request.get_json()
    encodedImage = data['imageEncoded']
    partnerId= int(data['partnerId'])
    name = data["name"]
    encoded_data = encodedImage.split(',')[1]
    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
    face_desc = get_face_embedding(imgRecovered)
    face_emb = vec2list(face_desc)
    update_table(name, face_emb, partnerId)
    response = Response(stream_with_context(json.dumps('Inserted successfully.')),mimetype='application/json')
    return response


