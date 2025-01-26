from flask import Blueprint, render_template, session
from utils import user

users_routes = Blueprint("users_routes", __name__)

@users_routes.route('/usermanagement', methods=['GET', 'POST']) # wil have to create page for members and adding
def user_management():
    user_role = user.get_role_by_username(session["user"])
    users_list = user.get_all_users()
    return render_template('user_management.html', role=user_role, users=users_list)

