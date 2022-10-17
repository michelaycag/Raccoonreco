from email import utils
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
from datetime import timedelta
from utils.utils import blocklist

initDB()

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.register_blueprint(routes, url_prefix="/api/v1")

app.config["JWT_SECRET_KEY"] = "secretKey"
app.config["JWT_TOKEN_LOCATION"] = [
    "headers", "query_string", "cookies", "json"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=6)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    for token in blocklist:
        if token == jti:
            return True
    return False


CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, I am Flask in Docker!'
