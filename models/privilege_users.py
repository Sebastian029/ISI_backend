from config import db

class Privilege_Users(db.Model):
    __tablename__ = 'privilege_users'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, primary_key=True)
    privilege_id = db.Column(db.Integer, db.ForeignKey('privilege.privilege_id'), nullable=False, primary_key=True)
    
    def to_json(self):
        return {
            "user_id": self.user_id,
            "privilege_id":self.privilege_id
        }