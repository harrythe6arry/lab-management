from psycopg2 import extras
from app.service import db, timezone


def get_all_tasks():
    """Fetch all tasks from the database."""
    conn = db.get_db_connection()
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    cur.execute("SELECT * FROM tasks ORDER BY id DESC;")
    tasks = cur.fetchall()
    db.close_db_connection(conn)

    # Convert UTC timestamps to Thailand time and format dates
    # add task that is overduem causes duplicates
    for task in tasks:
        if task['created_at']:
            task['created_at'] = timezone.convert_utc_to_thailand_time(task['created_at'])
        else:
            task['created_at'] = "Not Set"

        if task['completed_at']:
            task['completed_at'] = timezone.convert_utc_to_thailand_time(task['completed_at'])
        else:
            task['completed_at'] = "Not Set"

        if task['due_date']:
            task['due_date'] = timezone.convert_utc_to_thailand_time(task['due_date'])
        else:
            task['due_date'] = "Not Set"

        if task['due_date'] < timezone.get_thailand_time():
            task['status'] = 'Overdue'
            # update_task_status(task['id'], 'Overdue')

    return tasks


def add_task(name, due_date, status="Not Started", assigned_to=None):
    """Add a new task to the database."""

    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tasks (name, due_date, status, assigned_to, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (name, due_date, status, assigned_to, timezone.get_thailand_time()))
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        db.close_db_connection(conn)


def update_task(task_id, name=None, due_date=None, status=None, assigned_to=None):
    """Update an existing task."""
    try:
        print(
            f"Updating task ID: {task_id} with name: {name}, due_date: {due_date}, status: {status}, assigned_to: {assigned_to}")
        conn = db.get_db_connection()
        cur = conn.cursor()

        # Build the query and value list dynamically
        update_fields = []
        values = []
        if name is not None:
            update_fields.append("name = %s")
            values.append(name)
        if assigned_to is not None:
            update_fields.append("assigned_to = %s")
            values.append(assigned_to)
        if status is not None:
            update_fields.append("status = %s")
            values.append(status)
        if due_date is not None:
            update_fields.append("due_date = %s")
            values.append(due_date)

        # Ensure there's something to update
        if not update_fields:
            raise ValueError("No valid fields provided to update")

        values.append(task_id)

        print(f"Update query fields: {update_fields}")
        print(f"Update query values: {values}")

        # Build and execute the query
        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = %s"
        print(f"Executing query: {query} with values: {values}")
        cur.execute(query, values)
        conn.commit()
        print(f"Task ID: {task_id} updated successfully")
    except Exception as e:
        print(f"Error in update_task: {e}")
        conn.rollback()
        raise
    finally:
        db.close_db_connection(conn)


def delete_task(task_id):
    """Delete a task from the database."""
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        db.close_db_connection(conn)


def update_task_status(task_id, status):
    try:

        # Prepare the update query
        conn = db.get_db_connection()
        cur = conn.cursor()
        query = "UPDATE tasks SET status = %s WHERE id = %s"
        values = (status, task_id)

        # Execute the query
        cur.execute(query, values)

        # Commit the transaction to save the changes
        conn.commit()

        # Check how many rows were updated
        if cur.rowcount > 0:
            print(f"Task ID {task_id} updated successfully with status {status}")
        else:
            print(f"No task found with ID {task_id} to update.")

    except Exception as e:
        print(f"Error updating task: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
        db.close_db_connection(conn)
