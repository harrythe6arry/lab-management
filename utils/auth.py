import bcrypt
from . import user

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw

def verify_password(password, hashed_pw):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)

def login(username, password):
    hashed_pw = user.get_password_by_username(username)
    if not hashed_pw:
        return False
    return verify_password(password, hash_password(password))

