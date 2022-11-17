from wsgiref import headers
from flask import Flask
from routes import *
from urllib import response
import pytest
from app import app
from tokens import *


def test_insert_partner_without_all_fields():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        'name' : 'maik',
        'partnerId' : '888',
        'document' : '49787602',
    }

    response = app.test_client().post('/api/v1/partner',json=data, headers=headers)
    assert response.json['msg'] == "All fields are required!"
    assert response.status_code == 400

def test_insert_partner():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        'name' : 'maik',
        'partnerId' : '888',
        'document' : '49787602',
        'contactNumber':'0915959232',
    }

    response = app.test_client().post('/api/v1/partner',json=data, headers=headers)
    assert response.json['msg'] == "Partner inserted successfully"
    assert response.status_code == 201

def test_insert_partner_expired():
    headers = {
        'Authorization': 'Bearer {}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjY1Mjg2MSwianRpIjoiYjMyMDc2OGEtODAxMS00MDY5LWI5ZjgtNDg0YWEyM2U1OWVkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiZW1haWwiOiJtaWtlQG1pa2UuY29tIiwicm9sIjoiQWRtaW4ifSwibmJmIjoxNjY2NjUyODYxLCJjc3JmIjoiYjIxMmFlNDgtZTY1MC00YTE1LTgyZmMtMjQ0ODE1ZmZlMmJkIiwiZXhwIjoxNjY2NjUyOTEwfQ.hDLWVFMLN_SmoZ47PGp0pqlgXsgyxPESijIa7kOXXu8')
    }
    data = {
        'name' : 'maik',
        'partnerId' : '888',
        'document' : '49787602',
        'contactNumber':'0915959232',
    }

    response = app.test_client().post('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "Token has expired"
    assert response.status_code == 401

def test_insert_partner_unauthorized():
    headers = {
        'Authorization': 'Bearer {}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjY1Mjg2MSwianRpIjoiYjMyMDc2OGEtODAxMS00MDY5LWI5ZjgtNDg0YWEyM2U1OWVkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiZW1haWwiOiJtaWtlQG1pa2UuY29tIiwicm9sIjoiQWRtaW4ifSwibmJmIjoxNjY2NjUyODYxLCJjc3JmIjoiYjIxMmFlNDgtZTY1MC00YTE1LTgyZmMtMjQ0ODE1ZmZlMmJkIiwiZXhwIjoxNjY2NjUyOTEwfQ.hDLWVFMLN_SmoZ47PGp0pqlgXsgyxPESijIa7kOXXu8')
    }
    data = {
        'name' : 'maik',
        'partnerId' : '888',
        'document' : '49787602',
        'contactNumber':'0915959232',
    }

    response = app.test_client().post('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "Token has expired"
    assert response.status_code == 401


def test_edit_partner():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        'name' : 'maik',
        'partnerId': '888',
        'document' : '49787602',
        'contactNumber' : '8674867',
        'authorized' : 'Yes',

    }

    response = app.test_client().patch('/api/v1/partner',json=data, headers=headers)
    assert response.json['msg'] == "Partner updated successfully"
    assert response.status_code == 200

