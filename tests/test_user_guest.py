from tokens import *

def test_insert_user_guest():
    token = get_token_not_admin()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        'name' : 'maik',
        'email' : 'maik@guest.com',
        'password':'facu1234',
        'rol' : 'User',
    }

    response = app.test_client().post('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "Only admins can do that!"
    assert response.status_code == 401


def test_edit_user_guest():
    token = get_token_not_admin()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/user/maik@guest.com', headers=headers)
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
    assert response.json['msg'] == "Only admins can do that!"
    assert response.status_code == 401

def test_delete_user_guest():
    token = get_token_not_admin()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/user/maik@guest.com', headers=headers)
    id =  response.json['id']
    data = {
        "id": id
    }


    data = {
        'id': id,
    }

    response = app.test_client().delete('/api/v1/user',json=data, headers=headers)
    assert response.json['msg'] == "Only admins can do that!"
    assert response.status_code == 401
