from flask import Flask
from routes import routes
app = Flask(__name__)
app.register_blueprint(routes)
app.secret_key = "VERY_SECRET_KEY"  # will defo change this later

if __name__ == "__main__":
    app.run(debug=True)