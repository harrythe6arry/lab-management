import psycopg2
from utils import db
#
# def get_available_rooms(selected_date, timeslot):
#     try:
#         with db.get_db_connection() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                       SELECT * FROM rooms
#                         WHERE id NOT IN (
#                             SELECT item_id FROM bookings
#                             WHERE type = %s AND date = %s AND time_slot = %s
#                         )
#                 """, ("room", selected_date, timeslot))
#                 conn.commit()
#                 return cur.fetchall()
#     except psycopg2.Error as e:
#         print(f"[ERROR] Failed to get available room: {e}")
#         return []
#
# def get_available_equipment(selected_date, timeslot):
#     try:
#         with db.get_db_connection() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                       SELECT * FROM equipment
#                         WHERE id NOT IN (
#                             SELECT item_id FROM bookings
#                             WHERE type = %s AND date = %s AND time_slot = %s
#                         )
#                 """, ("equipment", selected_date, timeslot))
#                 conn.commit()
#                 return cur.fetchall()
#     except psycopg2.Error as e:
#         print(f"[ERROR] Failed to get available equipment: {e}")
#         return []
#
# def validate_quantity(equipment_id, selected_date, timeslot):
#     try:
#         with db.get_db_connection() as conn:
#             with conn.cursor() as cur:
#             # count how many quipment has been book with the same selected date and timeslot
#                 count_amount_booked_query = """
#                 SELECT COUNT(*) FROM bookings
#                 WHERE item_id = %s AND type = %s AND date = %s AND time_slot = %s
#                 """
#                 cur.execute(count_amount_booked_query, (equipment_id, "equipment", selected_date, timeslot))
#                 conn.commit()
#                 print("count" + cur.fetchone()[0])
#                 return cur.fetchone()[0]
#     except psycopg2.Error as e:
#         print(f"[ERROR] Failed to validate quantity: {e}")
#         return None

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
                    SELECT * FROM equipment
                    WHERE id NOT IN (
                        SELECT item_id FROM bookings
                        WHERE type = %s AND date = %s AND time_slot = %s
                    )
                """, ("equipment", selected_date, timeslot))
                return cur.fetchall()  # No need for commit()
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
                    SELECT COUNT(*) FROM bookings
                    WHERE item_id = %s AND type = 'equipment' AND date = %s AND time_slot = %s
                """, (equipment_id, selected_date, timeslot))
                booked_quantity = cur.fetchone()[0]
                is_available = available_quantity - booked_quantity >= quantity
                db.close_db_connection(conn)
                return True if is_available else False
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to validate quantity: {e}")
        return None



def book_room_and_equipment(name, room_id, equipments, date, timeslot):
    # Book the room and equipment here
    # Example: Insert booking data into the database for the room
    # booking_query = """
    # INSERT INTO bookings (name, type, date, timeslot, quantity, item_id)
    # VALUES (%s, %s, %s, %s, %s, %s);
    # """
    # db.execute(booking_query, (name, "room", date, timeslot, 1, room_id))
    #
    # # Insert equipment bookings
    # for eq in equipments:
    #     booking_equipment_query = """
    #     INSERT INTO booking (name, type, date, timeslot, quantity, item_id)
    #     VALUES (%s, %s, %s, %s, %s, %s);
    #     """
    #     db.execute(booking_equipment_query, (name, "equipment", date, timeslot, eq[1], room_id))

    # print all input data
    print(f"Booking room '{room_id}' for '{name}' on {date} at {timeslot}")
    print(f"Booking equipment: {equipments}")

    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cur:
                # Insert room booking and return room ID
                cur.execute("""
                      INSERT INTO bookings (name, type, date, timeslot, quantity, item_id)
                      VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                  """, (name, "room", date, timeslot, 1, room_id))
                room_booking_id = cur.fetchone()[0]  # Fetch the returned room booking ID

                # Insert equipment bookings and collect their IDs
                equipment_ids = []
                for eq in equipments:
                    equipment_name, quantity = eq
                    cur.execute("""
                        INSERT INTO bookings (name, type, date, timeslot, quantity, item_id)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                    """, (name, "equipment", date, timeslot, quantity, equipment_name))
                    equipment_ids.append(cur.fetchone()[0])

                conn.commit()
                db.close_db_connection(conn)
                return room_booking_id, equipment_ids
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to book room and equipment: {e}")
        return None, []



