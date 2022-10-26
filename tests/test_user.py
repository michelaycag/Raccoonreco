from wsgiref import headers
from flask import Flask
from routes import *
from urllib import response
import pytest
from app import app



def get_token():
    data = {
        'email' : 'mike@mike.com',
        'password':'facu1234'
    }
    response = app.test_client().post('/api/v1/login', json=data)
    
    return response.json['access_token']

def get_token_refresh():
    data = {
        'email' : 'mike@mike.com',
        'password':'facu1234'
    }
    response = app.test_client().post('/api/v1/login', json=data)
    
    return response.json['refresh_token']

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

def test_get_email():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/user/mike@mike.com', headers=headers)

    assert response.json['email'] == "mike@mike.com"
    assert response.json['id'] == 1
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
