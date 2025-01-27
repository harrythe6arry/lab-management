from flask import redirect, url_for, Blueprint, session, request, render_template
from Utils import user, auth

auth_routes = Blueprint("auth_routes", __name__)

def user_login_required(f):
    def wrap(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth_routes.login"))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Preserve function name
    return wrap

def admin_login_required(f):
    def wrap(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth_routes.login"))  # Redirect to login page if not logged in
        if user.get_role_by_username(session["user"]) != "Admin":
            return redirect(url_for("dashboard.dashboard"))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if auth.login(username, password):
            print("Login successful")
            session["user"] = username
            return redirect(url_for("dashboard_routes.dashboard"))
        else:
            print("Login failed")
            error_message = "Invalid username or password"  # Define the error message

    # Pass the error message to the template
    return render_template('login.html', error=error_message)

@auth_routes.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("auth_routes.login"))