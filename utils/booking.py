import psycopg2
from utils import db


def get_available_rooms(selected_date, timeslot):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM rooms
                    WHERE id NOT IN (
                        SELECT item_id FROM bookings
                        WHERE type = %s AND date = %s AND time_slot = %s
                    )
                """, ("room", selected_date, timeslot))
                return cur.fetchall()  # No need for commit()
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to get available room: {e}")
        return []

def get_available_equipment(selected_date, timeslot):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.id, e.name
                    FROM equipment e
                    LEFT JOIN (
                        SELECT item_id, SUM(quantity) AS booked_quantity
                        FROM bookings
                        WHERE type = 'equipment' AND date = %s AND time_slot = %s
                        GROUP BY item_id
                    ) b ON e.id = b.item_id
                    WHERE e.total_quantity > COALESCE(b.booked_quantity, 0)
                """, (selected_date, timeslot))
                return cur.fetchall()
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to get available equipment: {e}")
        return []

def validate_equipment_quantity(equipment_id, quantity, selected_date, timeslot):

    print(f"equipment_id: {equipment_id}, selected_date: {selected_date}, timeslot: {timeslot}, quantity: {quantity}")

    try:
        # Query the database to check available quantity
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT total_quantity FROM equipment WHERE id = %s
                """, (equipment_id,))
                available_quantity = cur.fetchone()[0]

                cur.execute("""
                    SELECT SUM(quantity) FROM bookings
                    WHERE item_id = %s AND type = 'equipment' AND date = %s AND time_slot = %s
                """, (equipment_id, selected_date, timeslot))
                booked_quantity = cur.fetchone()[0]
                print(f"available_quantity: {available_quantity}, booked_quantity: {booked_quantity}")
                if booked_quantity is None:
                    booked_quantity = 0
                is_available = available_quantity - booked_quantity >= quantity
                return True if is_available else False
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to validate quantity: {e}")
        return None
