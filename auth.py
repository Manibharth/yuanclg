import bcrypt

# Step 2: Import our database connection function
from db_config import get_connection


# ══════════════════════════════════════════════════════════
# FUNCTION 1: Register a new user
# ══════════════════════════════════════════════════════════
def register_user(username, email, password, full_name=""):

    # Step 3: Basic validation — check fields are not empty
    if not username or not email or not password:
        return False, "All fields are required."

    # Step 4: Hash the password using bcrypt
    #         bcrypt.hashpw() takes bytes, so we encode the string first
    #         gensalt() generates a random salt to make each hash unique
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Step 5: Get a database connection
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        # Step 6: Create a cursor — it's the object that sends SQL queries
        cursor = conn.cursor()

        # Step 7: Write the INSERT SQL with %s placeholders
        #         NEVER format values directly into SQL → SQL Injection risk!
        sql = """
            INSERT INTO users (username, email, password, full_name)
            VALUES (%s, %s, %s, %s)
        """

        # Step 8: Execute query with values as a tuple
        #         decode() converts bytes hash back to string for storage
        cursor.execute(sql, (username, email, hashed.decode('utf-8'), full_name))

        # Step 9: Commit saves the changes to the database permanently
        conn.commit()

        return True, f"✅ Account created! Welcome, {username}!"

    except Exception as e:
        # Step 10: If duplicate username/email, MySQL throws IntegrityError
        error_msg = str(e)
        if "Duplicate" in error_msg:
            return False, "❌ Username or Email already exists."
        return False, f"❌ Registration failed: {error_msg}"

    finally:
        # Step 11: Always close cursor and connection in 'finally'
        #          Guard with locals() check in case cursor was never created
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()


# ══════════════════════════════════════════════════════════
# FUNCTION 2: Login an existing user
# ══════════════════════════════════════════════════════════
def login_user(username, password):
    """
    Verifies username and password against the database.

    Parameters:
        username (str): Entered username
        password (str): Plain text password to verify

    Returns:
        (True,  user_dict)        on success — dict with user info
        (False, "Error message")  on failure
    """

    # Step 12: Validate inputs
    if not username or not password:
        return False, "Username and password are required."

    # Step 13: Get DB connection
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        # Step 14: Create cursor with dictionary=True
        #          This makes each row come back as a dict like {'id': 1, 'username': 'yuan'}
        cursor = conn.cursor(dictionary=True)

        # Step 15: SELECT the user by username
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (username,))  # Note: comma makes it a tuple

        # Step 16: fetchone() gets the first matching row, or None if not found
        user = cursor.fetchone()

        # Step 17: Check if user exists — if None, username is wrong
        #          WITHOUT this check, user['password'] below will crash!
        if not user:
            return False, "❌ Username not found."

        # Step 18: Verify the entered password against the stored hash
        #          bcrypt.checkpw() handles the comparison safely
        stored_hash = user['password'].encode('utf-8')  # Convert str to bytes
        entered_pw  = password.encode('utf-8')           # Convert str to bytes

        if bcrypt.checkpw(entered_pw, stored_hash):
            # Step 19: Password matches — return user data (exclude password field)
            user.pop('password')  # Remove password from the returned dict for safety
            return True, user     # Return user info to the GUI

        else:
            return False, "❌ Incorrect password."

    except Exception as e:
        return False, f"❌ Login error: {str(e)}"

    finally:
        # Step 20: Always close resources
        #          Guard with locals() check in case cursor was never created
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()