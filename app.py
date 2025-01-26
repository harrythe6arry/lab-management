from flask import Flask
from routes import auth, dashboard, tasks, users, inventory
app = Flask(__name__)
app.register_blueprint(auth.auth_routes)
app.register_blueprint(dashboard.dashboard_routes)
app.register_blueprint(tasks.tasks_routes)
app.register_blueprint(users.users_routes)
app.register_blueprint(inventory.inventory_routes)

app.secret_key = "VERY_SECRET_KEY"  # will defo change this later

if __name__ == "__main__":
    app.run(debug=True)