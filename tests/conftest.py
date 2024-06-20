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
        yield flask_app
        db.drop_all()

@pytest.fixture(scope='function')
def setup_database(app):
    with app.app_context():
        user1 = User(
            name="John",
            surname="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            password="password"
        )
        user1.public_id = "1"
        user2 = User(
            name="John2",
            surname="Doe2",
            phone_number="1234567899",
            email="john.doe2@example.com",
            password="password"
        )
        user2.public_id = "2"

        privilege = Privilege(name="buying")
        db.session.add(privilege)

        role = Role(name="admin")
        role2 = Role(name="user")
        db.session.add(role)
        db.session.add(role2)
        user1.roles.append(role)
        user1.privileges.append(privilege)
        user2.roles.append(role2)
        db.session.add_all([user1, user2])
        db.session.commit()

@pytest.fixture(scope='function')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def get_token(app_context):
    return generate_access_token("1", ["admin"], "John", "Doe")

@pytest.fixture(scope='function')
def get_token_user(app_context):
    return generate_access_token("2", ["user"], "John2", "Doe2")



@pytest.fixture(scope='function')
def app_context(app):
    with app.app_context():
        yield

