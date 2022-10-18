from pydoc import doc
from flask import jsonify, request
from FaceRecognitionFunctions import *
from . import routes
from flask_jwt_extended import jwt_required


@routes.route("/partner", methods=['POST'])
@jwt_required(fresh=True)
def insertPartner():
    name = request.json.get("name", None)
    partnerId = int(request.json.get("partnerId", None))
    document = request.json.get("document", None)
    contactNumber = request.json.get("contactNumber", None)
    authorized = True

    if name is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if partnerId is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if document is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if contactNumber is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute("INSERT INTO partners (name, partnerId, document,authorized , contactNumber) VALUES (%s,%s,%s,%s,%s)",
                    (name, partnerId, document, authorized, contactNumber))
        cur.execute(
            "SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
        user = cur.fetchone()
        con.commit()
        cur.close()
        return jsonify({"msg": "User inserted successfully", "user": user}), 201
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/partners", methods=['GET'])
@jwt_required(fresh=False)
def getAllPartners():
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM partners")
        users = cur.fetchall()
        con.commit()
        cur.close()
        usuarios = []
        if users is not None:
            for u in users:
                data = {}
                data["id"] = u[0]
                data["name"] = u[1]
                data["partnerId"] = u[2]
                data["document"] = u[3]
                data["authorized"] = u[4]
                data["contactNumber"] = u[5]
                usuarios.append(data)
        return jsonify({"data": usuarios}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/partner", methods=['PATCH'])
@jwt_required(fresh=True)
def updatePartner():
    name = request.json.get("name", None)
    partnerId = int(request.json.get("partnerId", None))
    document = request.json.get("document", None)
    contactNumber = request.json.get("contactNumber", None)

    if name is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if partnerId is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if document is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if contactNumber is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute("UPDATE partners SET name= %s, document= %s, contactNumber= %s WHERE partnerId= %s",
                    (name, document, contactNumber, partnerId))
        cur.execute(
            "SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
        user = cur.fetchone()
        con.commit()
        cur.close()
        return jsonify({"msg": "User updated successfully", "user": user}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/partner", methods=['DELETE'])
@jwt_required(fresh=True)
def deletePartner():
    partnerId = int(request.json.get("partnerId", None))

    if partnerId is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute("DELETE FROM partners p WHERE p.partnerid=%s", [partnerId])
        rowsDeleted = cur.rowcount
        cur.execute(
            "SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
        con.commit()
        cur.close()
        if (rowsDeleted != 1):
            return jsonify({"msg": str(rowsDeleted) + " rows deleted"}), 200
        else:
            return jsonify({"msg": str(rowsDeleted) + " row deleted"}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
