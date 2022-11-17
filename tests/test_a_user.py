from wsgiref import headers
from flask import Flask
from routes import *
from urllib import response
import pytest
from app import app
from tokens import *

def test_init():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, I am Flask in Docker!'

def test_login():

    data = {
        'email' : 'mike@mike.com',
        'password':'facu1234'
    }
    response = app.test_client().post('/api/v1/login', json=data)
    
    token = response.json['access_token']

    assert len(token) > 0
    assert response.status_code == 200

def test_login_invalid():

    data = {
        'email' : 'mike@mike.com',
        'password':'facu12345665'
    }
    response = app.test_client().post('/api/v1/login', json=data)
    assert response.json['msg'] == "Email or password are wrong!"   
    assert response.status_code == 401   

def test_login_no_password():

    data = {
        'email' : 'mike@mike.com'
    }
    response = app.test_client().post('/api/v1/login', json=data)
    assert response.json['msg'] == "All fields are required!"   
    assert response.status_code == 400

def test_get_all_users_unauthorized():
    response = app.test_client().get('/api/v1/users')
    

    assert response.status_code == 401

def test_get_all_users_authorized():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/users', headers=headers)

    assert response.status_code == 200

def test_insert_user_without_all_fields():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        'name' : 'maik',
        'email' : 'maik@mike.com',
        'password':'facu1234',
    }

    response = app.test_client().post('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "All fields are required!"
    assert response.status_code == 400

def test_insert_user():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        'name' : 'maik',
        'email' : 'maik@mike.com',
        'password':'facu1234',
        'rol' : 'Admin',
    }

    response = app.test_client().post('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "User inserted successfully"
    assert response.status_code == 201

def test_insert_user_expired():
    headers = {
        'Authorization': 'Bearer {}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjY1Mjg2MSwianRpIjoiYjMyMDc2OGEtODAxMS00MDY5LWI5ZjgtNDg0YWEyM2U1OWVkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiZW1haWwiOiJtaWtlQG1pa2UuY29tIiwicm9sIjoiQWRtaW4ifSwibmJmIjoxNjY2NjUyODYxLCJjc3JmIjoiYjIxMmFlNDgtZTY1MC00YTE1LTgyZmMtMjQ0ODE1ZmZlMmJkIiwiZXhwIjoxNjY2NjUyOTEwfQ.hDLWVFMLN_SmoZ47PGp0pqlgXsgyxPESijIa7kOXXu8')
    }
    data = {
        'name' : 'maik',
        'email' : 'maik@mike.com',
        'password':'facu1234',
        'rol' : 'Admin',
    }

    response = app.test_client().post('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "Token has expired"
    assert response.status_code == 401

def test_edit_user():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/user/maik@mike.com', headers=headers)
    id =  response.json['id']
    data = {
        "id": id
    }


    data = {
        'name' : 'michael',
        'id': id,
        'email' : 'maik@mike.com',
        'rol' : 'Admin',
    }

    response = app.test_client().patch('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "User updated successfully"
    assert response.status_code == 200

def test_delete_user_id_none():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        
    }

    response = app.test_client().delete('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "All fields are required!"
    assert response.status_code == 400

def test_delete_user():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/user/maik@mike.com', headers=headers)
    id =  response.json['id']
    data = {
        "id": id
    }

    response = app.test_client().delete('/api/v1/user',json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['msg'] == "1 row deleted"



def test_get_email():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/user/mike@mike.com', headers=headers)

    assert response.json['email'] == "mike@mike.com"
    assert response.json['name'] == "mike"
    assert response.json['rol'] == "Admin"
    assert response.status_code == 200

def test_get_token_status_alive():
    token = get_token_refresh()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/status', headers=headers)

    assert response.json['alive'] == True
    assert response.status_code == 200

def test_get_token_status_dead():
    headers = {
        'Authorization': 'Bearer {}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjY1Mjg2MSwianRpIjoiYjMyMDc2OGEtODAxMS00MDY5LWI5ZjgtNDg0YWEyM2U1OWVkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiZW1haWwiOiJtaWtlQG1pa2UuY29tIiwicm9sIjoiQWRtaW4ifSwibmJmIjoxNjY2NjUyODYxLCJjc3JmIjoiYjIxMmFlNDgtZTY1MC00YTE1LTgyZmMtMjQ0ODE1ZmZlMmJkIiwiZXhwIjoxNjY2NjUyOTEwfQ.hDLWVFMLN_SmoZ47PGp0pqlgXsgyxPESijIa7kOXXu8')
    }

    response = app.test_client().get('/api/v1/status', headers=headers)
    assert response.status_code == 401
    assert response.json['msg'] == 'Token has expired'


def test_insert_user_guest():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        'name' : 'maikguest',
        'email' : 'mike@guest.com',
        'password':'facu1234',
        'rol' : 'User',
    }

    response = app.test_client().post('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "User inserted successfully"
    assert response.status_code == 201
