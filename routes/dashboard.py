from flask import render_template, Blueprint
from psycopg2 import extras
from utils import db
from .auth import user_login_required

dashboard_routes = Blueprint("dashboard_routes", __name__)

@dashboard_routes.route('/dashboard')
@dashboard_routes.route('/')
@user_login_required
def dashboard():
    """
    Render the dashboard with summarized data and metrics.
    """
    try:
        # Connect to the database
        conn = db.get_db_connection()
        cur = conn.cursor(cursor_factory=extras.DictCursor)

        # Example metrics for the dashboard
        cur.execute("SELECT COUNT(*) AS total_inventory_items FROM inventory;")
        total_inventory_items = cur.fetchone()['total_inventory_items']

        cur.execute("""
            SELECT COUNT(*) AS low_stock_items 
            FROM inventory 
            WHERE amount <= threshold;
        """)
        low_stock_items = cur.fetchone()['low_stock_items']

        cur.execute("""
            SELECT ingredient, amount, threshold
            FROM inventory 
            WHERE amount <= threshold
            ORDER BY amount ASC
            LIMIT 5;
        """)
        low_stock_list = cur.fetchall()

        cur.execute("""
            SELECT ingredient, amount, last_updated, updated_by
            FROM inventory
            ORDER BY last_updated DESC
            LIMIT 5;
        """)
        recent_updates = cur.fetchall()

        # Close database connection
        db.close_db_connection(conn)

        # Pass all metrics to the dashboard template
        return render_template(
            'dashboard.html',
            total_inventory_items=total_inventory_items,
            low_stock_items=low_stock_items,
            low_stock_list=low_stock_list,
            recent_updates=recent_updates,
        )

    except Exception as e:
        # Handle errors gracefully
        print(f"Error fetching dashboard data: {e}")
        return render_template('error.html', error="Failed to load dashboard data.")



