
import unittest
from flask import Flask
from flask_testing import TestCase
from app.config import db
from app.models.user import User
from app.models.privilege import Privilege

class BaseTestCase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        self.user = User(
            name="John",
            surname="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            password="password"
        )
        db.session.add(self.user)
        self.privilege = Privilege(name="admin")
        db.session.add(self.privilege)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()