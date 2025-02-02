# Lab Management

## Description
Lab Management is a Flask-based web application designed to manage laboratory resources, bookings, and user authentication efficiently.

## Features
- User authentication and authorization
- Inventory management
- Task and booking system
- Dashboard for managing lab operations
- Calendar view for bookings
- User Management

## Project Structure
```
lab-management/
│── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── tasks.py
│   │   ├── users.py
│   │   ├── inventory.py
│   │   ├── booking.py
│   ├── static/
│   ├── templates/
│   ├── utils/
│   ├── __init__.py
│── .gitignore
│── poetry.lock
│── pyproject.toml
│── README.md
```

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/lab-management.git
cd lab-management
```

### 2. Download Poetry
```bash
pip install poetry
```

### 3. Install Dependencies
Using Poetry:
```bash
poetry install
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add necessary configurations like:
```ini
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_connection_string
```

## Running the Application
```bash
flask run
```