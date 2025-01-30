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
        return jsonify({'rooms': [room[1] for room in available_rooms]})
    return jsonify({'rooms': []})


@booking_routes.route('/api/available/equipments', methods=['GET'])
def get_available_equipments():
    selected_date = request.args.get('date')
    timeslot = request.args.get('timeslot')
    available_equipment = booking.get_available_equipment(selected_date, timeslot)
    print(available_equipment)
    if available_equipment:
        return jsonify({'equipment': [eq[1] for eq in available_equipment]})
    return jsonify({'equipment': []})

@booking_routes.route('/api/validate', methods=['POST'])
def validate_quantity():
    data = request.json
    equipment_id = data['equipment_id']
    quantity = data['quantity']
    selected_date = data['date']
    timeslot = data['timeslot']

    # Query to validate quantity
    equipment = validate_quantity((equipment_id, selected_date, timeslot))
    if equipment and equipment.total_quantity >= quantity:
        return jsonify({'valid': True})
    return jsonify({'valid': True})


@booking_routes.route('/api/book', methods=['POST'])
def submit_booking():
    data = request.json
    name = data['name']
    date = data['date']
    timeslot = data['timeslot']
    room = data['room']
    equipment = data['equipment']

    # Deduct the booked quantity of each equipment
    for eq in equipment:
        equipment_id = eq['name']
        quantity = eq['quantity']

        # Call the backend function to check and deduct the equipment
        result = booking.deduct_equipment_quantity(equipment_id, quantity, date, timeslot)
        if not result:
            return jsonify({'success': False, 'message': f"Not enough {equipment_id} available"})

    # Call the backend function to book the room and equipment
    booking_result = booking.book_room_and_equipment(name, room, equipment, date, timeslot)

    if booking_result:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Booking failed. Please try again.'})
