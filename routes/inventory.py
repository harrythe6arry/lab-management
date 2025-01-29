from flask import render_template, request, jsonify, session, Blueprint
from datetime import datetime
from utils import timezone, inventory
from routes.auth import user_login_required

inventory_routes = Blueprint("inventory_routes", __name__)

@inventory_routes.route('/inventory', methods=['GET'])
@user_login_required
def view_inventory():
    """Display inventory page with all items."""
    inventory_data = inventory.get_all_inventory_items()
    now = timezone.convert_utc_to_thailand_time(datetime.now())
    return render_template('inventory.html', inventory_data=inventory_data, now=now)

@inventory_routes.route('/inventory/add', methods=['POST'])
@user_login_required
def add_inventory_item_route():
    """Handle new item creation."""
    ingredient = request.form.get('ingredient')
    amount = request.form.get('amount')
    threshold = request.form.get('threshold')
    updated_by = session.get('user')

    try:
        new_id = inventory.add_inventory_item(ingredient, amount, threshold, updated_by)
        return jsonify({'success': True, 'id': new_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_routes.route('/inventory/edit', methods=['POST'])
@user_login_required
def edit_inventory_item_route():
    """Handle updating an inventory item."""
    item_id = request.form.get('id')
    ingredient = request.form.get('ingredient')
    amount = request.form.get('amount')
    threshold = request.form.get('threshold')
    updated_by = session.get('user')


    try:
        inventory.update_inventory_item(item_id, ingredient, amount, threshold, updated_by)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_routes.route('/inventory/delete', methods=['POST'])
@user_login_required
def delete_inventory_item_route():
    """Handle item deletion."""
    item_id = request.form.get('id')
    if not item_id:
        return jsonify({'error': 'Missing item ID'}), 400

    try:
        success = inventory.delete_inventory_item(item_id)
        if not success:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500