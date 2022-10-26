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


def test_recognize_face_unauthorized():
    data = {
        'encodedImage' : 'mike@mike.com',
        'parterId':'facu1234',
        'name':'facu1234'
    }
    response = app.test_client().post('/api/v1/face', json=data)
    
    assert response.status_code == 401

def chuelmo_recognize_face_unauthorized():
    data = {
        'encodedImage' : 'mike@mike.com',
        'parterId':'facu1234',
        'name':'facu1234'
    }
    response = app.test_client().post('/api/v1/face', json=data)
    
    assert response.status_code == 401

def test2_recognize_face_unauthorized():
    data = {
        'encodedImage' : 'mike@mike.com',
        'parterId':'facu1234',
        'name':'facu1234'
    }
    response = app.test_client().post('/api/v1/face', json=data)
    
    assert response.status_code == 401