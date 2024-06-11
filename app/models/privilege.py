from app.config import db

class Privilege(db.Model):
    privilege_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def to_json(self):
        return {
            "privilege_id": self.privilege_id,
            "name":self.name,
        }