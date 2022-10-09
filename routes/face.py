import cv2
from FaceEmbeddings import update_table
from FaceRecognitionFunctions import *
from flask import request,  Response, stream_with_context, jsonify
import base64
import json
from imageio import imread
import io
from . import routes
from flask_jwt_extended import jwt_required

@routes.route('/face', methods=['PUT'])
@jwt_required()
def compareImage():
    encodedImage = request.json.get('imageEncoded', None)
    
    if encodedImage is None:
        return jsonify({"msg": "All fields are required!"}), 400


    encoded_data = encodedImage.split(',')[1]

    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
    face_desc = get_face_embedding(imgRecovered)
    face_emb = vec2list(face_desc)
    retrieveResponse = retrieve(face_emb)
    response = Response(stream_with_context(json.dumps(retrieveResponse)), mimetype='application/json')
    return response


@routes.route('/face', methods=['POST'])
@jwt_required()
def insertFace():
    encodedImage = request.json.get('imageEncoded', None)
    partnerId= int(request.json.get('partnerId', None))
    name = request.json.get('name', None)

    if encodedImage is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if partnerId is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if name is None:
        return jsonify({"msg": "All fields are required!"}), 400

    encoded_data = encodedImage.split(',')[1]
    imgRecovered = imread(io.BytesIO(base64.b64decode(encoded_data)))
    imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
    face_desc = get_face_embedding(imgRecovered)
    face_emb = vec2list(face_desc)
    update_table(name, face_emb, partnerId)
    response = Response(stream_with_context(json.dumps('Inserted successfully.')),mimetype='application/json')
    return response


