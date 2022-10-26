from pydoc import doc
import re
import bcrypt
from flask import jsonify, request
from FaceRecognitionFunctions import *
from . import routes
from flask_jwt_extended import (JWTManager, get_jwt, jwt_required,
                                create_access_token, get_jwt_identity,
                                create_refresh_token, decode_token)
from utils.utils import blocklist
from datetime import datetime


@routes.route("/user", methods=['POST'])
@jwt_required(fresh=True)
def insertUser():
    current_user = get_jwt_identity()
    rolActual = current_user["rol"]
    if rolActual != "Admin":
        return {"msg": 'Only admins can do that!'}, 401

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
        hashedPassword = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        cur = con.cursor()
        cur.execute("INSERT INTO users (name, email, password, rol) VALUES (%s,%s,%s,%s)",
                    (name, email, hashedPassword.decode('utf-8'), rol))
        cur.execute("SELECT * from users u WHERE u.email = %s", [email])
        user = cur.fetchone()
        con.commit()
        cur.close()
        return jsonify({"msg": "User inserted successfully", "user": user}), 201
    except psycopg2.DatabaseError as e:
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
            return {"msg": 'Email or password are wrong!'}, 401
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            identidad = {"email": user[2], "rol": user[4]}
            access_token = create_access_token(
                identity=identidad, fresh=True)
            refresh_token = create_refresh_token(identidad)
            return {
                "msg": "Logged successfully",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {"msg": 'Email or password are wrong!'}, 401

    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/users", methods=['GET'])
@jwt_required(fresh=False)
def getAllUsers():
    try:
        cur = con.cursor()
        cur.execute("SELECT id, name, email, rol FROM users")
        users = cur.fetchall()
        con.commit()
        cur.close()
        usuarios = []
        if users is not None:
            for u in users:
                data = {}
                data["id"] = u[0]
                data["name"] = u[1]
                data["email"] = u[2]
                data["rol"] = u[3]
                usuarios.append(data)
        return jsonify({"data": usuarios}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/user", methods=['PATCH'])
@jwt_required(fresh=True)
def updateUser():
    current_user = get_jwt_identity()
    rolActual = current_user["rol"]
    if rolActual != "Admin":
        return {"msg": 'Only admins can do that!'}, 401

    name = request.json.get("name", None)
    id = int(request.json.get("id", None))
    rol = request.json.get("rol", None)
    email = request.json.get("email", None)

    if name is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if email is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if rol is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if id is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute(
            "UPDATE users SET name= %s, email= %s, rol= %s WHERE id = %s", (name, email, rol, id))
        cur.execute("SELECT * from users u WHERE u.email = %s", [email])
        user = cur.fetchone()
        con.commit()
        cur.close()
        return jsonify({"msg": "User updated successfully", "user": user}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/user", methods=['DELETE'])
@jwt_required(fresh=True)
def deleteUser():
    current_user = get_jwt_identity()
    rolActual = current_user["rol"]
    if rolActual != "Admin":
        return {"msg": 'Only admins can do that!'}, 401

    id = request.json.get("id", None)
    

    if id is None:
        return jsonify({"msg": "All fields are required!"}), 400
    else:
        id = int(id)

    try:
        cur = con.cursor()
        cur.execute("DELETE FROM users u WHERE u.id=%s", [id])
        rowsDeleted = cur.rowcount
        cur.execute("SELECT * from users u WHERE u.id = %s", [id])
        con.commit()
        cur.close()
        if (rowsDeleted != 1):
            return jsonify({"msg": str(rowsDeleted) + " rows deleted"}), 200
        else:
            return jsonify({"msg": str(rowsDeleted) + " row deleted"}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/refresh", methods=['GET'])
@jwt_required(refresh=True)
def refreshToken():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    return {'access_token': new_token}, 200


@routes.route("/fullRefresh", methods=['POST'])
@jwt_required(fresh=False)
def fullRefreshToken():
    password = request.json.get("password", None)

    if password is None:
        return jsonify({"msg": "Password is required!"}), 400
    current_user = get_jwt_identity()
    email = current_user["email"]
    cur = con.cursor()
    cur.execute("SELECT * from users u WHERE u.email = %s", [email])
    user = cur.fetchone()
    cur.close()
    if not user:
        return {"msg": 'Please login!'}, 401
    if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        identidad = {"email": user[2], "rol": user[4]}
        access_token = create_access_token(identity=identidad, fresh=True)
        refresh_token = create_refresh_token(identidad)
        return {
            "msg": "Refresh token successfully",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200
    return {"msg": 'Password is wrong!'}, 401


@routes.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    blocklist.add(jti)
    refreshToken = request.json.get("token", None)
    if refreshToken is not None:
        decode_token(refreshToken)
        blocklist.add(decode_token(refreshToken)["jti"])
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@routes.route("/user/<email>", methods=['GET'])
@jwt_required(fresh=False)
def getUserByEmail(email):
    if email is None:
        return jsonify({"msg": "email is required!"}), 400
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, name, email, rol from users u WHERE u.email = %s", [email])
        user = cur.fetchone()
        cur.close()
        if (user is not None and len(user) > 0):
            return jsonify({"id": user[0], "name": user[1], "email": user[2], "rol": user[3]}), 200
        return jsonify({"id": user}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/user", methods=['GET'])
@jwt_required(fresh=False)
def getUser():
    current_user = get_jwt_identity()
    email = current_user["email"]
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, name, email, rol from users u WHERE u.email = %s", [email])
        user = cur.fetchone()
        cur.close()
        if (user is not None and len(user) > 0):
            return jsonify({"id": user[0], "name": user[1], "email": user[2], "rol": user[3]}), 200
        return jsonify({"id": user}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/status", methods=['GET'])
@jwt_required(refresh=True)
def status():
    return jsonify({"alive": True}), 200
