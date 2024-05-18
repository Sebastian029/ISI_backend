from config import db

class Role_Users(db.Model):
    __tablename__ = 'role_users'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False, primary_key=True)
    
    def to_json(self):
        return {
            "user_id": self.user_id,
            "role_id":self.role_id
        }