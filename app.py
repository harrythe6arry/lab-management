from flask import Flask
from flask_bcrypt import Bcrypt
from routes import auth, dashboard, tasks, users, inventory
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.register_blueprint(auth.auth_routes)
app.register_blueprint(dashboard.dashboard_routes)
app.register_blueprint(tasks.tasks_routes)
app.register_blueprint(users.users_routes)
app.register_blueprint(inventory.inventory_routes)

app.secret_key = os.getenv('SECRET_KEY')

if __name__ == "__main__":
    app.run(debug=True)