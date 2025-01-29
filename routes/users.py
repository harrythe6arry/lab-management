from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from utils import user

users_routes = Blueprint("users_routes", __name__)

@users_routes.route('/usermanagement', methods=['GET', 'POST']) # wil have to create page for members and adding
def user_management():
    user_role = user.get_role_by_username(session["user"])
    users_list = user.get_all_users()
    return render_template('user_management.html', role=user_role, users=users_list)

@users_routes.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        print(f"Adding user: {username}")
        try:
            if user.insert_user(username, password, role):
                print("User inserted successfully")
                return jsonify({"message": "User created successfully"}), 201
            else:
                return jsonify({"message": "Failed to create user"}), 500
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return jsonify({"message": "Username already exists"}), 400
            else:
                return jsonify({"message": "An error occurred"}), 500
    return render_template('add_user.html')

@users_routes.route('/deleteuser', methods=['POST'])
def delete_user():
    data = request.get_json()
    username = data.get('username')
    # if the user is trying to delete themselves, return an error
    if username == session["user"]:
        return jsonify({"message": "You cannot delete yourself"}), 400
    print(f"Deleting user: {username}")
    if user.delete(username):
        print("User deleted successfully")
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "Failed to delete user"}), 500