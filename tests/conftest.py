import pytest
from app.models.user import User
from app.models.privilege import Privilege
from app import create_app
from app.config import db
from app.utils  import generate_access_token
from app.models.role import Role

@pytest.fixture()
def app():
    flask_app = create_app("sqlite://")

    flask_app.config['TESTING'] = True

    with flask_app.app_context():
        db.create_all()

        user = User(
            name="John",
            surname="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            password="password"
        )
        user.public_id = "1"

        user2 = User(
            name="John2",
            surname="Doe2",
            phone_number="1234567899",
            email="john.doe2@example.com",
            password="password"
        )
        user2.public_id = "2"
        db.session.add(user2)
        privilege = Privilege(name="buying")
        db.session.add(privilege)

        role = Role(name="admin")
        db.session.add(role)
        user.roles.append(role)
        user.privileges.append(privilege)
        db.session.add(user)
        db.session.commit()

    yield flask_app

    with flask_app.app_context():
        db.drop_all()

@pytest.fixture(scope='function')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def get_token(app_context):
    return generate_access_token("1")

@pytest.fixture(scope='function')
def app_context(app):
    with app.app_context():
        yield

