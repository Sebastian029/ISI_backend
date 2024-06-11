import unittest
from tests.base_test import BaseTestCase
from app.config import db
from app.models.user import User
from app.controllers.privilegeController import *
import json
from app.services.privilageService import *


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
        response = self.client.get(
            "/" )
        print(response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
