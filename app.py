import os
import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host=os.getenv('DB_HOST'),
                            database=os.getenv('DB_NAME'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))
    return conn
@app.route('/')
def hello_world():
    return render_template('base.html')

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

