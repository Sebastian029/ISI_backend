import unittest
from base_test import BaseTestCase
from controllers.userController import (
    check_password_controller, get_user_by_email, get_user_by_number,
    get_user_by_id, get_all_users, get_user_by_search, get_all_users_json,
    get_users_search, get_user_by_public_id, get_data_users_json,
    update_user, delete_user, change_notification, change_data
)

class UserTestCase(BaseTestCase):

    def test_check_password_controller(self):
        self.assertTrue(check_password_controller(self.user, "password"))
        self.assertFalse(check_password_controller(self.user, "wrongpassword"))

    def test_get_user_by_email(self):
        user = get_user_by_email("john.doe@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "john.doe@example.com")

    # Repeat other tests for user functions

if __name__ == '__main__':
    unittest.main()