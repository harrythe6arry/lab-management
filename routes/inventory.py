from flask import render_template, redirect, url_for, request, jsonify, Blueprint, session
from datetime import datetime
from psycopg2 import extras
from Utils import timezone, db
from routes.auth import user_login_required

inventory_routes = Blueprint("inventory_routes", __name__)


@inventory_routes.route('/inventory', methods=['GET'])
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

@inventory_routes.route('/inventory/add', methods=['POST'])
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

@inventory_routes.route('/inventory/edit', methods=['POST'])
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

@inventory_routes.route('/inventory/delete', methods=['POST'])
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

