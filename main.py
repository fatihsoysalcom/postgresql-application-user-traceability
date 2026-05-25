import os
import psycopg2
from psycopg2 import Error

# Database connection details from environment variables
DB_NAME = os.getenv("PG_DB_NAME", "postgres")
DB_USER = os.getenv("PG_DB_USER", "postgres")
DB_PASSWORD = os.getenv("PG_DB_PASSWORD", "password")
DB_HOST = os.getenv("PG_DB_HOST", "localhost")
DB_PORT = os.getenv("PG_DB_PORT", "5432")

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True # For DDL operations and immediate visibility
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        exit(1)

def setup_database(cursor):
    """Creates a test table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensitive_data (
            id SERIAL PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("Table 'sensitive_data' ensured.")

def cleanup_database(cursor):
    """Drops the test table."""
    cursor.execute("DROP TABLE IF EXISTS sensitive_data;")
    print("Table 'sensitive_data' dropped.")

def perform_action_as_user(conn, app_user, data):
    """
    Simulates an application user performing an action.
    Sets 'application_name' to identify the real user.
    """
    try:
        cursor = conn.cursor()
        # --- ARTICLE'S CORE CONCEPT ILLUSTRATION ---
        # Set the 'application_name' session variable to identify the actual application user.
        # This allows tools like pgAudit (if configured to log application_name)
        # to capture the real user, not just the database role used for connection.
        cursor.execute(f"SET application_name = '{app_user}';")
        print(f"\n--- Simulating action by application user: {app_user} ---")
        print(f"Set session application_name to '{app_user}'.")

        # Perform a data modification operation
        cursor.execute("INSERT INTO sensitive_data (data) VALUES (%s);", (data,))
        print(f"Inserted data '{data}' into sensitive_data table.")

        # Demonstrate that application_name is visible in pg_stat_activity
        # In a real pgAudit setup, this information would be logged.
        cursor.execute("SELECT usename, application_name, client_addr, state, query FROM pg_stat_activity WHERE pid = pg_backend_pid();")
        activity = cursor.fetchone()
        if activity:
            print(f"Current session activity (from pg_stat_activity):")
            print(f"  DB User: {activity[0]}, App Name: {activity[1]}, Client: {activity[2]}, State: {activity[3]}")
        else:
            print("Could not retrieve current session activity.")

    except Error as e:
        print(f"Error performing action for {app_user}: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

if __name__ == "__main__":
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cleanup_database(cursor) # Ensure a clean slate
        setup_database(cursor)

        # Simulate actions by different application users
        perform_action_as_user(conn, "Alice", "Alice's sensitive record")
        perform_action_as_user(conn, "Bob", "Bob's confidential document")

        print("\n--- Verification: Data in table ---")
        cursor.execute("SELECT id, data, created_at FROM sensitive_data;")
        records = cursor.fetchall()
        for record in records:
            print(f"ID: {record[0]}, Data: {record[1]}, Created At: {record[2]}")

    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            print("\nCleaning up database...")
            try:
                cursor = conn.cursor()
                cleanup_database(cursor)
                cursor.close()
            except Error as e:
                print(f"Error during cleanup: {e}")
            finally:
                conn.close()
                print("Database connection closed.")
