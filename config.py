import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # PostgreSQL URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoid overhead
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # For session management