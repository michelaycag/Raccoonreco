from pydoc import doc
from flask import jsonify, request, make_response, request
from FaceRecognitionFunctions import *
from . import routes
from flask_jwt_extended import jwt_required
import csv
import io
import base64
import requests
from imageio import imread
from FaceEmbeddings import update_table
import validators

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

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
        cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
        partner = cur.fetchone()
        if partner is not None:
            cur.close()
            return jsonify({"msg": "Duplicated partner Id"}), 409
        cur.execute("INSERT INTO partners (name, partnerId, document, authorized, contactNumber) VALUES (%s,%s,%s,%s,%s)",
                    (name, partnerId, document, authorized, contactNumber))
        cur.execute(
            "SELECT id, name, partnerId, document, authorized, contactNumber from partners p WHERE p.partnerId = %s", [partnerId])
        partner = cur.fetchone()
        partner = {
            "id":partner[0],
            "name":partner[1],
            "partnerId":partner[2],
            "document":partner[3],
            "authorized":partner[4],
            "contactNumber":partner[5]
        }
        con.commit()
        cur.close()
        return jsonify({"msg": "Partner inserted successfully", "partner": partner}), 201
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500


@routes.route("/partner/batch", methods=['POST'])
@jwt_required(fresh=True)
def insertPartnerBatch():
    f = request.files.get("partners", None)
    print('asd')
    if f is None:
        return jsonify({"msg": "No file uploaded"}), 400

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    next(csv_input)
    partners = []
    for row in csv_input:
        if len(row) == 5:
            partner = {
                "name":row[0].strip(),
                "partnerId":row[1].strip(),
                "document":row[2].strip(),
                "contactNumber":row[3].strip(),
                "authorized": True,
                "picture": row[4].strip()
            }
            partners.append(partner)
    insertedPartners = []
    for partner in partners:
        try:
            cur = con.cursor()
            if not partner['partnerId'].isnumeric():
                return jsonify({"msg": "partnerId should be numeric"}), 400
            if not validators.url(partner['picture']):
                return jsonify({"msg": "Url is not valid"}), 400
            cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [partner['partnerId']])
            fetchedPartner = cur.fetchone()
            if fetchedPartner is not None:
                cur.close()
                return jsonify({"msg": "Duplicated partner Id"}), 409
            cur.execute("INSERT INTO partners (name, partnerId, document, authorized, contactNumber) VALUES (%s,%s,%s,%s,%s)",
                       ( partner['name'], partner['partnerId'], partner['document'], partner['authorized'], partner['contactNumber']))
            cur.execute(
                "SELECT id, name, partnerId, document, authorized, contactNumber from partners p WHERE p.partnerId = %s", [partner['partnerId']])
            createdPartner = cur.fetchone()
            createdPartner = {
                "id":createdPartner[0],
                "name":createdPartner[1],
                "partnerId":createdPartner[2],
                "document":createdPartner[3],
                "authorized":createdPartner[4],
                "contactNumber":createdPartner[5],
            }
            image = requests.get(partner["picture"]).content
            base64PartnerImage = base64.b64encode(image)
            imgRecovered = imread(io.BytesIO(base64.b64decode(base64PartnerImage)))
            imgRecovered = cv2.cvtColor(imgRecovered, cv2.COLOR_RGB2BGR)
            face_desc = get_face_embedding(imgRecovered)
            face_emb = vec2list(face_desc)
            if len(face_emb) == 0:
                 return jsonify({"msg": "No face detected"}), 400
            update_table(createdPartner['name'], face_emb, createdPartner['id'])
            con.commit()
            cur.close()
            insertedPartners.append(createdPartner)
        except psycopg2.DatabaseError as e:
            return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
    if len(insertedPartners) > 0:       
        return jsonify({"msg": "Partners inserted successfully", "partner": insertedPartners}), 201
    else:
        return jsonify({"msg": "No partners were inserted, please check the uploaded file"}), 400


@routes.route("/partners", methods=['GET'])
@jwt_required(fresh=False)
def getAllPartners():
    try:
        offset=  request.args.get("offset",None)
        partnerId=  request.args.get("partnerId",None)
        if offset is None:
            if partnerId is None:
                cur = con.cursor()
                cur.execute("SELECT * FROM partners ORDER BY id")
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
            else:
                cur = con.cursor()
                cur.execute("SELECT * FROM partners WHERE partnerId::text LIKE '%"+ partnerId + "%' ORDER BY id")
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
        if partnerId is None:
            cur = con.cursor()
            cur.execute("SELECT * FROM partners ORDER BY id LIMIT 5 OFFSET " + offset)
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
        else:
            cur = con.cursor()
            cur.execute("SELECT * FROM partners WHERE partnerId::text LIKE '%"+ partnerId + "%' ORDER BY id LIMIT 5 OFFSET " + offset)
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
    authorized= request.json.get("authorized", None)

    if name is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if partnerId is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if document is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if contactNumber is None:
        return jsonify({"msg": "All fields are required!"}), 400
    if authorized is None:
        return jsonify({"msg": "All fields are required!"}), 400

    try:
        cur = con.cursor()
        cur.execute("UPDATE partners SET name= %s, document= %s, contactNumber= %s, authorized= %s WHERE partnerId= %s",
                    (name, document, contactNumber, authorized, partnerId))
        cur.execute(
            "SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
        partner = cur.fetchone()
        partner = {
            "id":partner[0],
            "name":partner[1],
            "partnerId":partner[2],
            "document":partner[3],
            "authorized":partner[4],
            "contactNumber":partner[5]
        }
        con.commit()
        cur.close()
        return jsonify({"msg": "Partner updated successfully", "partner": partner}), 200
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
        cur.execute("SELECT * from partners p WHERE p.partnerId = %s", [partnerId])
        partner = cur.fetchone()
        if partner is None:
             return jsonify({"msg": "Partner not found", "error": e}), 404
        partner = {
            "id":partner[0],
            "name":partner[1],
            "partnerId":partner[2],
            "document":partner[3],
            "authorized":partner[4],
            "contactNumber":partner[5]
        }
        cur.execute("DELETE FROM partners p WHERE p.partnerid=%s", [partnerId])
        rowsDeleted = cur.rowcount
        con.commit()
        cur.close()
        if (rowsDeleted != 1):
            return jsonify({"msg": str(rowsDeleted) + " rows deleted", "partner": partner}), 200
        else:
            return jsonify({"msg": str(rowsDeleted) + " row deleted",  "partner": partner}), 200
    except psycopg2.DatabaseError as e:
        return jsonify({"msg": "Something went wrong! Please try again later", "error": e}), 500
