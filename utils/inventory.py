from psycopg2 import extras
from Utils import db, timezone

def get_all_inventory_items():
    """Fetch all inventory items from the database."""
    conn = db.get_db_connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT * FROM inventory ORDER BY id DESC;")
    inventory_data = cur.fetchall()
    db.close_db_connection(conn)

    # Convert UTC times to Thailand time
    for item in inventory_data:
        item['last_updated'] = timezone.convert_utc_to_thailand_time(item['last_updated'])

    return inventory_data

def add_inventory_item(ingredient, amount, threshold, updated_by):
    """Add a new item to the inventory."""
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO inventory (ingredient, amount, threshold, updated_by)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (ingredient, amount, threshold, updated_by))
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        db.close_db_connection(conn)

def update_inventory_item(item_id, ingredient, amount, threshold, updated_by):
    """Update an existing inventory item."""
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE inventory
            SET ingredient = %s, amount = %s, threshold = %s, 
                updated_by = %s, last_updated = %s
            WHERE id = %s
        """, (ingredient, amount, threshold, updated_by, timezone.get_thailand_time(), item_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        db.close_db_connection(conn)

def delete_inventory_item(item_id):
    """Delete an inventory item."""
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        db.close_db_connection(conn)