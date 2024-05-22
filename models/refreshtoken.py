from config import db

class RefreshToken(db.Model):
    refresh_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(512), nullable=False, unique=True)
    public_id = db.Column(db.String(36), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=False)

    def __init__(self, token, public_id, expires, revoked):
        self.token = token
        self.public_id = public_id
        self.expires = expires
        self.revoked = revoked