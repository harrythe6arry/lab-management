import os

from flask import Flask
from app.routes import auth, dashboard, tasks, users, inventory, booking

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth.auth_routes)
    app.register_blueprint(dashboard.dashboard_routes)
    app.register_blueprint(tasks.tasks_routes)
    app.register_blueprint(users.users_routes)
    app.register_blueprint(inventory.inventory_routes)
    app.register_blueprint(booking.booking_routes)
    app.secret_key = os.getenv('SECRET_KEY')
    return app
