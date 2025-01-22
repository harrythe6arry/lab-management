import bcrypt
from . import user

def hashed(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def login(username, password):
    hashed_password = user.get_password_by_username(username)
    if not hashed_password:
        return False
    return verify_password(password, hashed(password))