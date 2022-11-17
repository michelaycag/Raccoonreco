from test_sface import get_token
from app import app

def test_delete_user_guest():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = app.test_client().get('/api/v1/user/mike@guest.com', headers=headers)
    id =  response.json['id']
    data = {
        "id": id
    }

    response = app.test_client().delete('/api/v1/user',json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['msg'] == "1 row deleted"


def test_delete_partner():
    token = get_token()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    data = {
        "partnerId": 888
    }

    response = app.test_client().delete('/api/v1/partner',json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['msg'] == "1 row deleted"