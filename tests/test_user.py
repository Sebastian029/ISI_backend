import unittest
from base_test import BaseTestCase
from app.controllers.userController import *

class UserTestCase(BaseTestCase):

    def test_check_password_controller(self):
        self.assertTrue(check_password_controller(self.user, "password"))
        self.assertFalse(check_password_controller(self.user, "wrongpassword"))

    def test_get_user_by_email(self):
        user = get_user_by_email("john.doe@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "john.doe@example.com")

    def test_get_user_by_number(self):
        user = get_user_by_number("1234567890")
        self.assertIsNotNone(user)
        self.assertEqual(user.phone_number, "1234567890")

    def test_get_user_by_id(self):
        user = get_user_by_id(self.user.user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, self.user.user_id)

    def test_get_all_users(self):
        users = get_all_users()
        self.assertEqual(len(users), 1)

    def test_get_user_by_search(self):
        user_json = get_user_by_search("John", "Doe", "john.doe@example.com")
        self.assertIsNotNone(user_json)
        self.assertEqual(user_json['name'], "John")

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertEqual(len(users_json), 1)
        self.assertEqual(users_json[0]['email'], "john.doe@example.com")

    def test_get_users_search(self):
        users_search_json = get_users_search()
        self.assertEqual(len(users_search_json), 1)
        self.assertEqual(users_search_json[0]['name'], "John")

    def test_get_data_users_json(self):
        data_users_json = get_data_users_json()
        self.assertEqual(len(data_users_json), 1)
        self.assertEqual(data_users_json[0]['name'], "John")

    def test_update_user(self):
        updated_user = update_user(self.user.user_id, "54321", "Jane", "Smith", "0987654321", "jane.smith@example.com")
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.public_id, "54321")
        self.assertEqual(updated_user.name, "Jane")

    def test_delete_user(self):
        success = delete_user(self.user.user_id)
        self.assertTrue(success)
        self.assertIsNone(get_user_by_id(self.user.user_id))

    def test_change_notification(self):
        print(self.user.notification)
        user2 = change_notification(self.user)
        print(user2.notification)
        self.assertEqual(self.user.notification , user2.notification)

    def test_change_data(self):
        data = type('Data', (object,), {'phoneNumber': '1111111111', 'name': 'Johnny', 'surname': 'Doey'})()
        change_data(data, self.user)
        self.assertEqual(self.user.phone_number, '1111111111')
        self.assertEqual(self.user.name, 'Johnny')
        self.assertEqual(self.user.surname, 'Doey')

if __name__ == '__main__':
    unittest.main()