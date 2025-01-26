import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, jsonify
from psycopg2 import extras
from Utils.convert_time_zone import get_thailand_time


from Utils import auth, user

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(host=os.getenv('DB_HOST'),
                            database=os.getenv('DB_NAME'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))
    cur = conn.cursor()
    cur.execute("SET timezone = 'Asia/Bangkok';")  # Set timezone to Thailand
    conn.commit()
    return conn

app = Flask(__name__)



@app.route('/inventory', methods=['GET'])
def view_inventory():
    """Display inventory page with all items"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT * FROM inventory ORDER BY id DESC;")
    inventory_data = cur.fetchall()
    cur.close()
    conn.close()
    now = datetime.now()
    return render_template('inventory.html', inventory_data=inventory_data, now=now)

@app.route('/inventory/add', methods=['POST'])
def add_inventory_item():
    """Handle new item creation"""
    ingredient = request.form.get('ingredient')
    amount = request.form.get('amount')
    threshold = request.form.get('threshold')
    by = request.form.get('by')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO inventory (ingredient, amount, threshold, updated_by)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (ingredient, amount, threshold, by))
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({'success': True, 'new_id': new_id}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/inventory/edit', methods=['POST'])
def edit_inventory_item():

    item_id = request.form.get('id')
    ingredient = request.form.get('ingredient')
    amount = request.form.get('amount')
    threshold = request.form.get('threshold')
    by = request.form.get('by')


    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE inventory
            SET ingredient = %s, amount = %s, threshold = %s, 
                updated_by = %s, last_updated = %s
            WHERE id = %s
        """, (ingredient, amount, threshold, by, get_thailand_time(), item_id))
        conn.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/inventory/delete', methods=['POST'])
def delete_inventory_item():
    """Handle item deletion"""
    try:
        item_id = request.form.get('id')
        if not item_id:
            return jsonify({'error': 'Missing item ID'}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Delete the item from the database
        cur.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({'error': 'Item not found'}), 404

        return jsonify({'success': True}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cur.close()
        conn.close()



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        date = request.form.get('taskDate')
        equipment = request.form.get('equipment')
        team_members = request.form.get('teamMembers')

        print(f"Date: {date}, Equipment: {equipment}, Team Members: {team_members}")
        return redirect(url_for('home'))

    return render_template('task.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Username: {username}, Password: {password}")
        if auth.login(username, password):
            print("Login successful")
        return redirect(url_for('home'))  # Redirect after login
    return render_template('login.html')

@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # print(f"Username: {username}, Password: {password}")
        user.insert_user(username, password, 'Staff')
        # print("User successfully created")
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