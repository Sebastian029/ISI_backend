from app.config import db

class Token(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(256), nullable=False, unique=True)
    refresh_token = db.Column(db.String(256), nullable=False, unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)



    def __init__(self, user_id, access_token, refresh_token):
        self.user_id = user_id
        self.acess_token = access_token
        self.refresh_token = refresh_token