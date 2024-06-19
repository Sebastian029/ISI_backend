from app.config import db
from app.models.token import Token

def get_first_free_token_id():
    all_token_ids = db.session.query(Token.token_id).order_by(Token.token_id).all()
    all_token_ids = [row.token_id for row in all_token_ids]
    
    for index in range(1, len(all_token_ids) + 1):
        if index not in all_token_ids:
            return index
    
    return len(all_token_ids) + 1