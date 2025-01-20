import os
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="lab_management",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Create tables and insert sample data

# Create users table
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')

# Insert sample data into users table
cur.execute('''
    INSERT INTO users (name, email, password, role) VALUES
    ('test2', 'test2@example.com', 'test2', 'Staff'),
    ('test3', 'test3@example.com', 'test3', 'Manager')
    ON CONFLICT (email) DO NOTHING;
''')

# Create equipment table
cur.execute('''
    CREATE TABLE IF NOT EXISTS equipment (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        status VARCHAR(50) NOT NULL,
        last_cleaned_at TIMESTAMP,
        location VARCHAR(100)
    );
''')

# Insert sample data into equipment table
cur.execute('''
    INSERT INTO equipment (name, status, last_cleaned_at, location) VALUES
    ('Centrifuge', 'Available', '2024-12-10 10:00:00', 'Lab A'),
    ('Microscope', 'In Use', '2024-12-09 15:30:00', 'Lab B')
    ON CONFLICT (name) DO NOTHING;
''')

# Create cleaning_task table
cur.execute('''
    CREATE TABLE IF NOT EXISTS cleaning_task (
        id SERIAL PRIMARY KEY,
        equipment_id INTEGER REFERENCES equipment(id) ON DELETE CASCADE,
        assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
        status VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    );
''')

# Insert sample data into cleaning_task table
cur.execute('''
    INSERT INTO cleaning_task (equipment_id, assigned_to, status, completed_at) VALUES
    (1, 1, 'Pending', NULL),
    (2, 2, 'Completed', '2024-12-09 16:00:00')
    ON CONFLICT DO NOTHING;
''')

# Create inventory table
cur.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id SERIAL PRIMARY KEY,
        item_name VARCHAR(100) NOT NULL,
        quantity INTEGER NOT NULL,
        threshold INTEGER NOT NULL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')

# Insert sample data into inventory table
cur.execute('''
    INSERT INTO inventory (item_name, quantity, threshold) VALUES
    ('Petri dish', 200, 50),
    ('Gloves', 500, 100)
    ON CONFLICT (item_name) DO NOTHING;
''')

# Create schedule table
cur.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id SERIAL PRIMARY KEY,
        equipment_id INTEGER REFERENCES equipment(id) ON DELETE CASCADE,
        booked_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL,
        status VARCHAR(50) NOT NULL,
        notes TEXT
    );
''')

# Insert sample data into schedule table
cur.execute('''
    INSERT INTO schedule (equipment_id, booked_by, start_time, end_time, status) VALUES
    (1, 1, '2024-12-12 09:00:00', '2024-12-12 11:00:00', 'Confirmed'),
    (2, 2, '2024-12-13 14:00:00', '2024-12-13 16:00:00', 'Cancelled')
    ON CONFLICT DO NOTHING;
''')

# Create safety_checklist table
cur.execute('''
    CREATE TABLE IF NOT EXISTS safety_checklist (
        id SERIAL PRIMARY KEY,
        task TEXT NOT NULL,
        assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
        status VARCHAR(50) NOT NULL,
        deadline TIMESTAMP NOT NULL,
        completed_at TIMESTAMP
    );
''')

# Insert sample data into safety_checklist table
cur.execute('''
    INSERT INTO safety_checklist (task, assigned_to, status, deadline) VALUES
    ('Check fire extinguishers', 1, 'Pending', '2024-12-15 17:00:00'),
    ('Inspect safety goggles', 2, 'Completed', '2024-12-10 12:00:00')
    ON CONFLICT (task) DO NOTHING;
''')

# Create location table
cur.execute('''
    CREATE TABLE IF NOT EXISTS location (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        purpose TEXT,
        building VARCHAR(100)
    );
''')

# Insert sample data into location table
cur.execute('''
    INSERT INTO location (name, building) VALUES
    ('Lab A', 'Building 1'),
    ('Lab B', 'Building 2')
    ON CONFLICT (name) DO NOTHING;
''')

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Database initialized with sample data successfully!")
