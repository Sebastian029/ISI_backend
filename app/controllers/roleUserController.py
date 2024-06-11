from app.models.user import User
from app.config import db
from app.controllers.roleController import get_role
from app.controllers.privilegeController import get_privilages

def create_user( firstName, lastName, phone_number, email, password):
    new_user = User(name=firstName, surname=lastName, phone_number=phone_number, email=email, password=password)
    role = get_role(2)
    if role:
        new_user.roles.append(role)
    privilages = get_privilages()

    if privilages:
        for privilage in privilages:
            new_user.privileges.append(privilage)
    db.session.add(new_user)
    db.session.commit()
    return new_user