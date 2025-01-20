# Lab Management App

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Create a `.env` file and add your database credentials:
    ```bash
    DB_USERNAME=your_database_user
    DB_PASSWORD=your_database_password
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the database setup script to create the tables and insert sample data:
    ```bash
    python init_db.py
    ```

5. Start the application:
    ```bash
    python app.py
    ```

## Database Setup

The `init_db.py` script will create the necessary database tables and insert sample data.

## Troubleshooting

- If you encounter a database connection error, ensure your PostgreSQL instance is running and your credentials are correct.
