from pydoc import doc
import bcrypt
from flask import jsonify, request
from FaceRecognitionFunctions import *
from . import routes
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, create_access_token, get_jwt_identity


@routes.route("/user", methods=['POST'])
@jwt_required()
def insertUser():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    rol = request.json.get("rol", None)

    if name is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if email is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if password is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if rol is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur = con.cursor()
        cur.execute("INSERT INTO users (name, email, password, rol) VALUES (%s,%s,%s,%s)", (name, email, hashedPassword.decode('utf-8'), rol))
        cur.execute("SELECT * from users u WHERE u.email = %s", [email])
        user = cur.fetchone()
        con.commit()
        cur.close()
        return jsonify({"msg": "User inserted successfully", "user": user}), 201
    except psycopg2.DatabaseError as e :
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
    

@routes.route("/login", methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if password is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute("SELECT * from users u WHERE u.email = %s", [email])
        user = cur.fetchone()
        cur.close()
        if not user:
            return {"msg":'Email or password are wrong!'}, 401
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            access_token = create_access_token(identity={"email": user[2]})
            return {"msg": "Logged successfully", "access_token": access_token}, 200
        return {"msg":'Email or password are wrong!'}, 401

    except psycopg2.DatabaseError as e :
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500




@routes.route("/users", methods=['GET'])
@jwt_required()
def getAllUsers():
    try:
        cur = con.cursor()    
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        con.commit()
        cur.close()
        return jsonify({"data": users}), 200
    except psycopg2.DatabaseError as e :
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/user", methods=['PATCH'])
@jwt_required()
def updateUser():
    name = request.json.get("name", None)
    email = int(request.json.get("partnerId", None))
    password = request.json.get("password", None)
    rol = request.json.get("rol", None)

    if name is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if email is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if password is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if rol is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute("UPDATE users SET name= %s, email= %s, password= %s WHERE rol= %s", (name, email, password, rol))
        cur.execute("SELECT * from users u WHERE u.email = %s", [email])
        user = cur.fetchone()
        con.commit()
        cur.close()
        return jsonify({"msg": "User updated successfully", "user": user}), 200
    except psycopg2.DatabaseError as e :
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500



@routes.route("/user", methods=['DELETE'])
@jwt_required()
def deleteUser():
    email = request.json.get("email", None)

    if email is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute("DELETE FROM users u WHERE u.emai=%s", [email] )
        rowsDeleted = cur.rowcount
        cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [email])
        con.commit()
        cur.close()
        if (rowsDeleted != 1):
            return jsonify({"msg": str(rowsDeleted) + " rows deleted"}), 200
        else:
            return jsonify({"msg": str(rowsDeleted) + " row deleted"}), 200
    except psycopg2.DatabaseError as e :
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
