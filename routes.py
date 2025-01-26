import os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, jsonify, Blueprint, session
from psycopg2 import extras
from Utils import auth, user
from Utils.convert_time_zone import get_thailand_time

routes = Blueprint("routes", __name__)

def user_login_required(f):
    def wrap(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("routes.login"))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Preserve function name
    return wrap

def admin_login_required(f):
    def wrap(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("routes.login"))  # Redirect to login page if not logged in
        if user.get_role_by_username(session["user"]) != "Admin":
            return redirect(url_for("routes.dashboard"))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__ 
    return wrap

@app.route('/inventory', methods=['GET'])
@user_login_required
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
@user_login_required
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
@user_login_required
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
@user_login_required
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

@routes.route('/')
def home():
    return "Welcome! <a href='/dashboard'>Go to Dashboard</a>"

@routes.route('/dashboard')
@user_login_required
def dashboard():
    return render_template('home.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if auth.login(username, password):
            print("Login successful")
            session["user"] = username
            return redirect(url_for("routes.dashboard"))
    return render_template('login.html')

@routes.route('/logout')
@user_login_required
def logout():
    session.pop("user", None)
    return redirect(url_for("routes.login"))

@routes.route('/usermanagement', methods=['GET', 'POST']) # wil have to create page for members and adding
@admin_login_required
def add_user():
    return render_template('users.html')

@routes.route('/task', methods=['GET', 'POST'])
@user_login_required
def task():
    if request.method == 'POST':
        date = request.form.get('taskDate')
        equipment = request.form.get('equipment')
        team_members = request.form.get('teamMembers')

        print(f"Date: {date}, Equipment: {equipment}, Team Members: {team_members}")
        return redirect(url_for('routes.home'))  # Use Blueprint name

    return render_template('task.html')

@routes.route('/inventory', methods=['GET', 'POST'])
@user_login_required
def inventory():
    return render_template('inventory.html')