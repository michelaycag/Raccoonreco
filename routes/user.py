from pydoc import doc
from flask import jsonify, request
from FaceRecognitionFunctions import *
from . import routes


@routes.route("/user", methods=['POST'])
def register():
    name = request.json.get("name", None)
    partnerId = int(request.json.get("partnerId", None))
    document = request.json.get("document", None)
    contactNumber = request.json.get("contactNumber", None)


    if all(item is not None for item in [name, partnerId, document,contactNumber]):
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO partners (name, partnerId, document, contactNumber) VALUES (%s,%s,%s,%s)", (name, partnerId, document, contactNumber))
            cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
            user = cur.fetchone()
            con.commit()
            cur.close()
            return jsonify({"msg": "User inserted successfully", "user": user}), 201
        except psycopg2.DatabaseError as e :
            return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
    return jsonify({"msg": "All fields are required!"}), 400


@routes.route("/users", methods=['GET'])
def getAll():
    try:
        cur = con.cursor()    
        cur.execute("SELECT * FROM partners")
        users = cur.fetchall()
        con.commit()
        cur.close()
        return jsonify({"data": users}), 200
    except psycopg2.DatabaseError as e :
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/user", methods=['PATCH'])
def updateUser():
    name = request.json.get("name", None)
    partnerId = int(request.json.get("partnerId", None))
    document = request.json.get("document", None)
    contactNumber = request.json.get("contactNumber", None)


    if all(item is not None for item in [name, partnerId, document,contactNumber]):
        try:
            cur = con.cursor()
            cur.execute("UPDATE partners SET name= %s, document= %s, contactNumber= %s WHERE partnerId= %s", (name, document, contactNumber, partnerId))
            cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
            user = cur.fetchone()
            con.commit()
            cur.close()
            return jsonify({"msg": "User updated successfully", "user": user}), 200
        except psycopg2.DatabaseError as e :
            return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
    return jsonify({"msg": "All fields are required!"}), 400


@routes.route("/user", methods=['DELETE'])
def delete():
    partnerId = request.json.get("partnerId", None)
    if all(item is not None for item in [partnerId]):
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM partners p WHERE p.partnerid=%s", [partnerId] )
            rowsDeleted = cur.rowcount
            cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
            con.commit()
            cur.close()
            if (rowsDeleted != 1):
                return jsonify({"msg": str(rowsDeleted) + " rows deleted"}), 200
            else:
                return jsonify({"msg": str(rowsDeleted) + " row deleted"}), 200
        except psycopg2.DatabaseError as e :
            return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
    return jsonify({"msg": "All fields are required!"}), 400