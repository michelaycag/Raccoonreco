from pydoc import doc
from flask import jsonify, request
from FaceRecognitionFunctions import *
from . import routes


@routes.route("/register", methods=['POST'])
def register():
    name = request.json.get("name", None)
    partnerId = int(request.json.get("partnerId", None))
    document = request.json.get("document", None)
    contactNumber = request.json.get("contactNumber", None)


    if all(item is not None for item in [name, partnerId, document,contactNumber]):
        try:
            cur.execute("INSERT INTO partners (name, partnerId, document, contactNumber) VALUES (%s,%s,%s,%s)", (name, partnerId, document, contactNumber))
            cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
            user = cur.fetchone()
            con.commit()
            return jsonify({"msg": "User inserted successfully", "user": user}), 201
        except psycopg2.DatabaseError as e :
            con.commit()
            return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
    con.commit()
    return jsonify({"msg": "All fields are required!"}), 400

