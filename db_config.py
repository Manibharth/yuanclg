import mysql.connector

# Step 2: Import the 'Error' class to catch MySQL-specific errors
from mysql.connector import Error


# ─────────────────────────────────────────────
# Step 3: Define DB credentials in a dictionary
#         Change these values to match YOUR MySQL setup
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",       # MySQL server address (localhost = your own PC)
    "user":     "root",            # MySQL username
    "password": "yuan@123",        # MySQL password (leave "" if none)
    "database": "yuandatabase"     # The database name we created in setup.sql
}


# ─────────────────────────────────────────────
# Step 4: Define a function to create a connection
#         A function is used so we can call it anywhere we need a connection
# ─────────────────────────────────────────────
def get_connection():
    """
    Creates and returns a MySQL database connection.
    Returns: connection object on success, None on failure.
    """
    try:
        # Step 4a: Try to connect using the credentials from DB_CONFIG
        #          ** unpacks the dictionary as keyword arguments
        connection = mysql.connector.connect(**DB_CONFIG)

        # Step 4b: Check if connection is active using is_connected()
        if connection.is_connected():
            return connection  # Return the live connection object

    except Error as e:
        # Step 4c: If something goes wrong, print the error
        #          and return None so the caller knows it failed
        print(f"[DB ERROR] Could not connect: {e}")
        return None


# ─────────────────────────────────────────────
# Step 5: Test the connection when this file
#         is run directly (python db_config.py)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ Database connected successfully!")
        conn.close()  # Always close the connection when done
    else:
        print("❌ Connection failed. Check your credentials.")