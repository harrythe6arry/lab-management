from flask import Blueprint, render_template, request, jsonify
from utils import booking
booking_routes = Blueprint('booking_routes', __name__)

@booking_routes.route('/booking', methods=['GET'])
def booking_page():
    return render_template('booking.html')

@booking_routes.route('/api/available/rooms', methods=['GET'])
def get_available_rooms():
    selected_date = request.args.get('date')
    timeslot = request.args.get('timeslot')

    available_rooms = booking.get_available_rooms(selected_date, timeslot)
    print(available_rooms)
    if available_rooms:
        return jsonify({'rooms': [{'id': room[0], 'name': room[1]} for room in available_rooms]})
    return jsonify({'rooms': []})

@booking_routes.route('/api/available/equipments', methods=['GET'])
def get_available_equipments():
    selected_date = request.args.get('date')
    timeslot = request.args.get('timeslot')
    available_equipment = booking.get_available_equipment(selected_date, timeslot)
    print(available_equipment)
    if available_equipment:
        return jsonify({'equipments': [{'id': eq[0], 'name': eq[1]} for eq in available_equipment]})
    return jsonify({'equipments': []})

@booking_routes.route('/api/validate/quantity', methods=['GET'])
def validate_quantity():
    equipment_id = request.args.get('equipment_id')
    quantity = int(request.args.get('quantity'))
    selected_date = request.args.get('date')
    timeslot = request.args.get('timeslot')

    is_available = booking.validate_equipment_quantity(equipment_id, quantity, selected_date, timeslot)
    print(is_available)
    return jsonify({'isAvailable': is_available})


@booking_routes.route('/api/book', methods=['POST'])
def submit_booking():
    data = request.json
    print(data)
    name = data['name']
    date = data['date']
    timeslot = data['timeslot']
    room_id = data['room']
    equipments = data['equipments']

    booked_room_name, booked_equipments = booking.book_room_and_equipment(name, room_id, equipments, date, timeslot)

    if booked_room_name is None | booked_equipments is None:
        return jsonify({'error': 'Booking failed'}), 400

    return jsonify({
        "room_name": booked_room_name,
        "equipment_bookings": [{"equipment_name": eq_name, "quantity": qty} for eq_name, qty in booked_equipments]
    })

