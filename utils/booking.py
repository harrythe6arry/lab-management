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
                conn.commit()
                return cur.fetchall()
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to get available room: {e}")
        return []


def get_available_equipment(selected_date, timeslot):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                      SELECT * FROM equipment
                        WHERE id NOT IN (
                            SELECT item_id FROM bookings
                            WHERE type = %s AND date = %s AND time_slot = %s
                        )
                """, ("equipment", selected_date, timeslot))
                conn.commit()
                return cur.fetchall()
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to get available equipment: {e}")
        return []


def validate_quantity(equipment_id, selected_date, timeslot):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                      SELECT quantity FROM equipment
                        WHERE id = %s AND date = %s AND time_slot = %s
                """, (equipment_id, selected_date, timeslot))
                conn.commit()
                return cur.fetchone()
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to validate quantity: {e}")
        return None

def deduct_equipment_quantity(equipment_name, quantity, date, timeslot):
    # Check if the quantity is available in the database for the given date and timeslot
    query = """
    SELECT quantity FROM equipment_table
    WHERE name = %s AND date = %s AND timeslot = %s;
    """
    result = db.execute(query, (equipment_name, date, timeslot))
    if result and result[0]['total_quantity'] >= quantity:
        # Deduct the quantity
        update_query = """
        UPDATE equipment_table
        SET quantity = quantity - %s
        WHERE name = %s AND date = %s AND timeslot = %s;
        """
        db.execute(update_query, (quantity, equipment_name, date, timeslot))
        return True
    return False

def book_room_and_equipment(name, room, equipment, date, timeslot):
    # Book the room and equipment here
    # Example: Insert booking data into the database for the room
    booking_query = """
    INSERT INTO bookings (name, room, date, timeslot)
    VALUES (%s, %s, %s, %s);
    """
    db.execute(booking_query, (name, room, date, timeslot))

    # Insert equipment bookings
    for eq in equipment:
        equipment_query = """
        INSERT INTO equipment_bookings (booking_id, equipment_name, quantity)
        VALUES (LAST_INSERT_ID(), %s, %s);
        """
        db.execute(equipment_query, (eq['name'], eq['quantity']))

    return True


