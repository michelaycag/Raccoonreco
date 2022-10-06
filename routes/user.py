import cv2
from FaceEmbeddings import update_table
from FaceRecognitionFunctions import *
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
import json
from codecs import encode
from imageio import imread
import io
from createSQLfunctions import initDB
from . import routes


@routes.route("/register", methods=['POST', 'GET'])
def register():
    return 'Hello, I am in register'
