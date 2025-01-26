from flask import Flask
from routes import routes  # Import the Blueprint

app = Flask(__name__)
app.register_blueprint(routes)  # Register routes

if __name__ == "__main__":
    app.run(debug=True)