import json
from app.controllers.privilegeController import *
from app.models.user import User
from app.models.privilege import Privilege


def test_get_privilages(setup_database):
    privileges = get_privilages()
    assert len(privileges) == 1
    assert privileges[0].name == "buying"
    
def test_get_privilege_by_name(setup_database):
    privilege = get_privilege_by_name("buying")
    assert privilege is not None
    assert privilege.name == "buying"

def test_get_privilages_json(setup_database):
    privileges_json = get_privilages_json()
    assert(len(privileges_json), 1)
    assert(privileges_json[0]['name'], "buying")

def test_remove_privilege(setup_database):
    user = User.query.filter_by(public_id='1').first()
    response, status_code = remove_privilege(user.public_id, "buying")
    assert status_code == 200
    assert response == "Privilege removed successfully"

def test_add_privilege(setup_database):
    user = User.query.filter_by(public_id='2').first()  
    response, status_code = add_privilege(user.public_id, "buying")
    assert status_code == 200
    assert response == "Privilege added successfully"

#endpointy

def test_get_privileges_route(setup_database,test_client, get_token):
    headers = {
        'x-access-tokens': get_token
    }
    response = test_client.get("/privilages", headers=headers)
    assert response.status_code == 200
    assert 'buying' in response.json[0]['name']

def test_get_users_privileges(setup_database,test_client, get_token):
    headers = {
        'x-access-tokens': get_token
    }
    response = test_client.get("/users/privilages", headers=headers)
    assert response.status_code == 200
    assert response.json[0]['email'] == 'john.doe@example.com'

def test_add_user_privilege(setup_database,test_client, get_token):
    headers = {
        'x-access-tokens': get_token,
        'Content-Type': 'application/json'
    }
    data = {
        'public_id': '2',
        'privilege_name': 'buying'
    }
    response = test_client.post("/users/privileges/add", headers=headers, data=json.dumps(data))
    assert response.status_code == 200
    assert response.json['message'] == 'Privilege added successfully'

def test_remove_user_privilege(setup_database,test_client, get_token):
    headers = {
        'x-access-tokens': get_token,
        'Content-Type': 'application/json'
    }
    data = {
        'public_id': '1',
        'privilege_name': 'buying'
    }
    response = test_client.delete("/users/privileges/remove", headers=headers, data=json.dumps(data))
    assert response.status_code == 200
    assert response.json['message'] == 'Privilege removed successfully'
