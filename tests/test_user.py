from app.controllers.userController import *
from app.models.user import User
from app.models.privilege import Privilege

from types import SimpleNamespace
import json

def test_check_password_controller(setup_database):
    user = get_user_by_email("john.doe@example.com")
    assert check_password_controller(user, "password") == True

def test_get_user_by_email(setup_database):
    user = get_user_by_email("john.doe@example.com")
    assert user is not None
    assert user.name == "John"

def test_get_user_by_number(setup_database):
    user = get_user_by_number("1234567890")
    assert user is not None
    assert user.name == "John"

def test_get_user_by_id(setup_database):
    user = get_user_by_id(2)
    assert user is not None
    assert user.name == "John2"

def test_get_all_users(setup_database):
    users = get_all_users()
    assert len(users) == 2

def test_get_user_by_search(setup_database):
    user = get_user_by_search("John", "Doe", "john.doe@example.com")
    assert user is not None
    assert user['name'] == "John"
    assert user['surname'] == "Doe"

def test_get_all_users_json(setup_database):
    users = get_all_users_json()
    assert len(users) == 2

def test_get_users_search(setup_database):
    users = get_users_search()
    assert len(users) == 2

def test_get_user_by_public_id(setup_database):
    user = get_user_by_public_id("1")
    assert user is not None
    assert user.name == "John"

def test_get_data_users_json(setup_database):
    users = get_data_users_json()
    assert len(users) == 1


def test_delete_user(setup_database):
    user = get_user_by_id(1)
    assert user is not None
    assert delete_user(user.user_id) == True
    assert get_user_by_id(1) is None

def test_change_notification(setup_database):
    user = get_user_by_id(1)
    assert user.notification == False
    updated_user = change_notification(user)
    assert updated_user.notification == True

def test_change_data(setup_database):
    user = get_user_by_id(1)
    json_data = '{"phoneNumber": "9999999999", "name": "Updated", "surname": "User"}'

    data = json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))

    print(data.phoneNumber)
    updated_user = change_data(data, user)
    assert updated_user.phone_number == '9999999999'
    assert updated_user.name == 'Updated'
    assert updated_user.surname == 'User'

#endpointy


def test_register_user(test_client, setup_database):
    data = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test.user@example.com",
        "phoneNumber": "098765432",  # Dokładnie 9 cyfr
        "password": "Password1!"  # Spełnia kryteria walidacji hasła
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = test_client.post("/register", data=json.dumps(data), headers=headers)
    
    # Dodanie logowania odpowiedzi serwera w przypadku niepowodzenia testu
    if response.status_code != 201:
        print(f"Response data: {response.data}")
    
    assert response.status_code == 201
    assert response.json["message"] == "User created!"

def test_update_notification(test_client, setup_database, get_token):
    headers = {
        "x-access-tokens": get_token
    }
    response = test_client.patch("/notification", headers=headers)
    assert response.status_code == 200

def test_update_user(test_client, setup_database, get_token):
    headers = {
        "x-access-tokens": get_token,
        'Content-Type': 'application/json'
    }
    data = {
        "name": "Updated",
        "surname": "User",
        "phoneNumber": "098765421"
    }
    response = test_client.patch("/update_user", data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json["message"] == "User updated successfully"

def test_delete_contact(test_client, setup_database):
    response = test_client.delete("/delete_contact/2")
    assert response.status_code == 200
    assert response.json["message"] == "User deleted!"

def test_get_contacts(test_client, setup_database, get_token):
    headers = {
        "x-access-tokens": get_token
    }
    response = test_client.get("/users", headers=headers)
    assert response.status_code == 200


def test_get_contact(test_client, setup_database, get_token):
    headers = {
        "x-access-tokens": get_token
    }
    response = test_client.get("/contact", headers=headers)
    assert response.status_code == 200


def test_get_users_search(test_client, setup_database):
    response = test_client.get("/users_search")
    assert response.status_code == 200

def test_get_contacts_email(test_client, setup_database):
    data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }
    response = test_client.post("/user_privileges", json=data)
    assert response.status_code == 200