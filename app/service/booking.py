import json
from tkinter.constants import INSERT

import psycopg2
from flask import session

import app.service.timezone
from app.service import db

def get_available_rooms(selected_date, timeslot):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM rooms
                    WHERE id NOT IN (
                        SELECT item_id FROM bookings
                        WHERE item_type = %s AND date = %s AND time_slot = %s
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
                        WHERE item_type = 'equipment' AND date = %s AND time_slot = %s
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
                    WHERE item_id = %s AND item_type = 'equipment' AND date = %s AND time_slot = %s
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


def book_room_and_equipment(name, room_id, room_name, equipments, date, timeslot):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO bookings (booking_name, item_type, date, time_slot, quantity, item_id)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                """, (name, "room", date, timeslot, 1, room_id))
                equipment_details = []
                for eq in equipments:
                    equipment_name, equipment_id, quantity = eq
                    cur.execute("""
                        INSERT INTO bookings (booking_name, item_type, date, time_slot, quantity, item_id)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                    """, (name, "equipment", date, timeslot, quantity, equipment_id))
                    equipment_details.append({
                        'name': equipment_name,
                        'quantity': quantity
                    })

                cur.execute("""
                    INSERT INTO schedule (booking_name, time_slot, booking_date, room, equipments, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                """, (name, timeslot, date, room_name, json.dumps(equipment_details), session['user']))
                conn.commit()
                return {
                    'room_name': room_name,
                    'equipment_booking_details': equipment_details
                }

    except psycopg2.Error as e:
        print(f"[ERROR] Failed to book room and equipment: {e}")
        return None

def get_all_bookings():
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM schedule")
                bookings = cur.fetchall()
                events = []
                for booking in bookings:
                    # Assuming booking[3] is the date and booking[2] is the time (adjust if your table is different)
                    start_datetime = booking[3]  # Assuming booking[3] is a datetime object



                    event = {
                        "id": booking[0],
                        "title": booking[1],  # Show only booking name
                        "start": f"{start_datetime.strftime('%Y-%m-%d')}T{booking[2]}",  # Date and time
                        "extendedProps": {
                            "room": booking[4],  # Room name
                            "equipments": booking[5] if booking[5] else [],  # List of equipment
                            "created_by": booking[6],  # Created by user
                            "created_at": app.service.timezone.convert_utc_to_thailand_time(booking[7]).strftime("%Y-%m-%d %H:%M:%S"),
                            "date": start_datetime.strftime('%Y-%m-%d'),
                            "timeslot": booking[2]
                        }
                    }
                    events.append(event)
                return events
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to get bookings: {e}")
        return []


def delete_booking(delete_id):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM bookings WHERE id = %s", (delete_id,))
                conn.commit()
                return True
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to delete booking: {e}")
        return False
    finally:
        db.close_db_connection(conn)