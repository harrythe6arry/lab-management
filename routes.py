from flask import render_template, redirect, url_for, request, jsonify, Blueprint, session
from datetime import datetime
from psycopg2 import extras
from utils import auth, user, timezone, db
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

@routes.route('/dashboard')
@routes.route('/')
@user_login_required
def dashboard():
    """
    Render the dashboard with summarized data and metrics.
    """
    try:
        # Connect to the database
        conn = db.get_db_connection()
        cur = conn.cursor(cursor_factory=extras.DictCursor)

        # Example metrics for the dashboard
        cur.execute("SELECT COUNT(*) AS total_inventory_items FROM inventory;")
        total_inventory_items = cur.fetchone()['total_inventory_items']

        cur.execute("""
            SELECT COUNT(*) AS low_stock_items 
            FROM inventory 
            WHERE amount <= threshold;
        """)
        low_stock_items = cur.fetchone()['low_stock_items']

        cur.execute("""
            SELECT ingredient, amount, threshold
            FROM inventory 
            WHERE amount <= threshold
            ORDER BY amount ASC
            LIMIT 5;
        """)
        low_stock_list = cur.fetchall()

        cur.execute("""
            SELECT ingredient, amount, last_updated, updated_by
            FROM inventory
            ORDER BY last_updated DESC
            LIMIT 5;
        """)
        recent_updates = cur.fetchall()

        # Close database connection
        db.close_db_connection(conn)

        # Pass all metrics to the dashboard template
        return render_template(
            'dashboard.html',
            total_inventory_items=total_inventory_items,
            low_stock_items=low_stock_items,
            low_stock_list=low_stock_list,
            recent_updates=recent_updates,
        )

    except Exception as e:
        # Handle errors gracefully
        print(f"Error fetching dashboard data: {e}")
        return render_template('error.html', error="Failed to load dashboard data.")


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
def logout():
    session.pop("user", None)
    return redirect(url_for("routes.login"))

@routes.route('/usermanagement', methods=['GET', 'POST']) # wil have to create page for members and adding
def user_management():
    user_role = user.get_role_by_username(session["user"])
    users_list = user.get_all_users()
    return render_template('user_management.html', role=user_role, users=users_list)

@routes.route('/task', methods=['GET', 'POST'])
@user_login_required
def task():
    if request.method == 'POST':
        date = request.form.get('taskDate')
        equipment = request.form.get('equipment')
        team_members = request.form.get('teamMembers')

        print(f"Date: {date}, Equipment: {equipment}, Team Members: {team_members}")
        return redirect(url_for('routes.home'))

    return render_template('task.html')

@routes.route('/inventory', methods=['GET'])
@user_login_required
def view_inventory():
    """Display inventory page with all items"""
    conn = db.get_db_connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT * FROM inventory ORDER BY id DESC;")
    inventory_data = cur.fetchall()
    db.close_db_connection(conn)
    now = datetime.now()
    return render_template('inventory.html', inventory_data=inventory_data, now=now)

@routes.route('/inventory/add', methods=['POST'])
@user_login_required
def add_inventory_item():
    """Handle new item creation"""
    ingredient = request.form.get('ingredient')
    amount = request.form.get('amount')
    threshold = request.form.get('threshold')
    by = request.form.get('by')

    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO inventory (ingredient, amount, threshold, updated_by)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (ingredient, amount, threshold, by))
        new_id = cur.fetchone()[0]

        conn.commit()
        return jsonify({'success': True, 'id': new_id}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close_db_connection(conn)

@routes.route('/inventory/edit', methods=['POST'])
@user_login_required
def edit_inventory_item():

    item_id = request.form.get('id')
    ingredient = request.form.get('ingredient')
    amount = request.form.get('amount')
    threshold = request.form.get('threshold')
    by = request.form.get('by')
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE inventory
            SET ingredient = %s, amount = %s, threshold = %s, 
                updated_by = %s, last_updated = %s
            WHERE id = %s
        """, (ingredient, amount, threshold, by, timezone.get_thailand_time(), item_id))
        conn.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close_db_connection(conn)

@routes.route('/inventory/delete', methods=['POST'])
@user_login_required
def delete_inventory_item():
    """Handle item deletion"""
    try:
        item_id = request.form.get('id')
        if not item_id:
            return jsonify({'error': 'Missing item ID'}), 400

        conn = db.get_db_connection()
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
        db.close_db_connection(conn)