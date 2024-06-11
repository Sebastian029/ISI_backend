
import unittest
from flask import Flask
from flask_testing import TestCase
from app.config import db
from app.models.user import User
from app.models.privilege import Privilege
from app.services.privilageService import *


class BaseTestCase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True

        db.init_app(app)
        
        with app.app_context():
            db.create_all()
        

        return app

    def setUp(self):
            self.app = self.create_app()
            self.app_context = self.app.app_context()
            self.app_context.push()
            db.create_all()
            self.client = self.app.test_client()
            self.user = User(
                name="John",
                surname="Doe",
                phone_number="1234567890",
                email="john.doe@example.com",
                password="password"
            )
            self.user.public_id = "1"
            db.session.add(self.user)
            self.privilege = Privilege(name="admin")
            db.session.add(self.privilege)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_token(self):
    # Normally, you would implement token generation and validation here.
    # For simplicity, we'll skip actual token handling and mock it.
        return "test-token"