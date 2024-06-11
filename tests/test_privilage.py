import unittest
from tests.base_test import BaseTestCase
from app.config import db
from app.models.user import User
from app.controllers.privilegeController import *
import json

class PrivilegeTestCase(BaseTestCase):

    def test_get_privilages(self):
        privileges = get_privilages()
        self.assertEqual(len(privileges), 1)
        self.assertEqual(privileges[0].name, "admin")

    def test_get_privilege_by_name(self):
        privilege = get_privilege_by_name("admin")
        self.assertIsNotNone(privilege)
        self.assertEqual(privilege.name, "admin")

    def test_get_privilages_json(self):
        privileges_json = get_privilages_json()
        self.assertEqual(len(privileges_json), 1)
        self.assertEqual(privileges_json[0]['name'], "admin")

    def test_remove_privilege(self):
        self.user.privileges.append(self.privilege)
        db.session.commit()
        response, status_code = remove_privilege(self.user.public_id, "admin")
        self.assertEqual(status_code, 200)
        self.assertEqual(response, "Privilege removed successfully")

    def test_add_privilege(self):
        response, status_code = add_privilege(self.user.public_id, "admin")
        self.assertEqual(status_code, 200)
        self.assertEqual(response, "Privilege added successfully")


    def test_get_privilages_route(self):
        response = self.client.get('/privilages')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_users_privilages_route(self):
        # First, log in the user to get a token
        response = self.client.post('/login', json={'email': 'john.doe@example.com', 'password': 'password'})
        token = json.loads(response.data)['token']

        response = self.client.get('/users/privilages', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_add_user_privilege_route(self):
        data = {
            'public_id': '12345',
            'privilege_name': 'admin'
        }
        response = self.client.post('/users/privileges/add', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Privilege added successfully', json.loads(response.data)['message'])

    def test_remove_user_privilege_route(self):
        data = {
            'public_id': '12345',
            'privilege_name': 'admin'
        }
        # First add the privilege to ensure it can be removed
        self.client.post('/users/privileges/add', json=data)

        response = self.client.delete('/users/privileges/remove', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Privilege removed successfully', json.loads(response.data)['message'])

if __name__ == '__main__':
    unittest.main()
