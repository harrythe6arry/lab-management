from psycopg2 import extras
from app.service import db, timezone


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
    """Add a new item to the inventory, summing amounts for duplicate ingredients."""
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        # print(f" ingredient: {ingredient}, amount: {amount}, threshold: {threshold}, updated_by: {updated_by}")

        cur.execute("""
            SELECT id, amount FROM inventory WHERE ingredient = %s
        """, (ingredient,))
        existing_item = cur.fetchone()
        # print(f"existing_item: {existing_item}")

        if existing_item:
            print(f"Ingredient found. Calculating new amount...")

            try:
                existing_amount = int(existing_item[1])  # Cast amount to integer
                new_amount = existing_amount + int(amount)  # Ensure new amount is also an integer
                print(f"Calculated new amount: {new_amount}")
            except ValueError as e:
                print(f"Error converting to integer: {e}")
                raise e

            cur.execute("""
                UPDATE inventory
                SET amount = %s, threshold = %s, updated_by = %s, last_updated = %s
                WHERE id = %s
            """, (new_amount, threshold, updated_by, timezone.get_thailand_time(), existing_item[0]))

            # print(f"Executed UPDATE query. New amount: {new_amount}, Threshold: {threshold}, Updated by: {updated_by}")
            new_id = existing_item[0]  # The id from the existing item
            # print(f"New ID to return: {new_id}")
            conn.commit()
            # print("Commit successful.")
            return new_id
        else:
            # If the ingredient does not exist, insert a new row
            print("Ingredient not found. Inserting new item.")
            cur.execute("""
                INSERT INTO inventory (ingredient, amount, threshold, updated_by)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (ingredient, amount, threshold, updated_by))

            # Fetch the new id from the insert result
            new_id = cur.fetchone()[0]
            print(f"New item inserted with ID: {new_id}")

            # Commit the transaction
            conn.commit()
            print("Commit successful.")
            return new_id

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
        raise e
    finally:
        db.close_db_connection(conn)
        print("Database connection closed.")


def update_inventory_item(item_id, ingredient, amount, threshold, updated_by):
    """Update an existing inventory item."""
    try:
        # print(f" item_id: {item_id}, ingredient: {ingredient}, amount: {amount}, threshold: {threshold}, updated_by: {updated_by}")

        conn = db.get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT update_inventory_item(
                %s, -- item_id
                %s::VARCHAR(100), -- ingredient
                %s::INTEGER, -- amount
                %s::INTEGER, -- threshold
                %s::VARCHAR(100), -- updated_by
                %s::TIMESTAMP -- last_updated
            );
        """, (item_id, ingredient, amount, threshold, updated_by, timezone.get_thailand_time()))

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
