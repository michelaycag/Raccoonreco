from socket import timeout
import psycopg2
import cv2
import dlib
from psycopg2.extras import execute_values
import os
from FaceEmbeddings import cam_exec
from FaceRecognitionFunctions import *


name = "Harbhajan_Singh"
# img = dlib.load_rgb_image(work_dir + name + '/' + name + '_0001.jpg')
img = dlib.load_rgb_image("./LFW/14_Aaron_Johnson_0001.jpg")
face_desc = get_face_embedding(img)
face_emb = vec2list(face_desc)


# retrieve busca la string de cosos en la base de datos
print(retrieve(face_emb))
