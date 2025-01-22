from dotenv import load_dotenv
import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, request, jsonify

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(host=os.getenv('DB_HOST'),
                            database=os.getenv('DB_NAME'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))
    return conn

app = Flask(__name__)


@app.route('/task', methods=['GET', 'POST'])
@app.route('/task')
def task():
    if request.method == 'POST':
        date = request.form.get('taskDate')
        equipment = request.form.get('equipment')
        team_members = request.form.get('teamMembers')

        print(f"Date: {date}, Equipment: {equipment}, Team Members: {team_members}")
        return redirect(url_for('home'))

    return render_template('task.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Placeholder logic: Validate these credentials
        print(f"Username: {username}, Password: {password}")
        return redirect(url_for('home'))  # Redirect after login
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

@app.route('/equipment')
def equipment():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, status, last_cleaned_at, location FROM equipment;')
    equipment_list = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('equipment.html', equipment_list=equipment_list)
