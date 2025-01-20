from flask import Flask, render_template, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Placeholder logic: Validate these credentials
        print(f"Username: {username}, Password: {password}")
        return redirect(url_for('hello_world'))  # Redirect after login
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Placeholder logic: Store these credentials in your database securely
        print(f"Username: {username}, Password: {password}")
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()