from config import db

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def to_json(self):
        return {
            "role_id": self.user_id,
            "name":self.name,
        }