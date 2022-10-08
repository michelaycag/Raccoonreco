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
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

initDB()

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.register_blueprint(routes,url_prefix="/api/v1")

app.config["JWT_SECRET_KEY"] = "secretKey"
jwt = JWTManager(app)


CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, I am Flask in Docker!'
