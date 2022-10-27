
from app import app

def get_token():
    data = {
        'email' : 'mike@mike.com',
        'password':'facu1234'
    }
    response = app.test_client().post('/api/v1/login', json=data)
    
    return response.json['access_token']

def get_token_not_admin():
    data = {
        'email' : 'mike@guest.com',
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
