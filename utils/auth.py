from utils import user
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

def login(username, password):
    hashed_pw = user.get_password_by_username(username)
    if hashed_pw is None:
        return False
    return check_password_hash(hashed_pw, password)