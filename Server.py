from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

# ── Import auth helpers ────────────────────────────────────────────────
from auth import register_user, login_user

# ── Import DB connection directly for the extra endpoints ─────────────
from db_config import get_connection


# ══════════════════════════════════════════════════════════════════════
# APP SETUP
# ══════════════════════════════════════════════════════════════════════

app = Flask(__name__)

# Allow the browser (index.html) to call this server from any origin.
# In production, replace "*" with your exact front-end domain.
CORS(app)


# ══════════════════════════════════════════════════════════════════════
# UTILITY HELPERS
# ══════════════════════════════════════════════════════════════════════

def is_valid_email(email: str) -> bool:
    """Basic email format check using a simple regex."""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(pattern, email))


def success_response(data: dict, status: int = 200):
    """Return a standard success JSON response."""
    return jsonify({"success": True, **data}), status


def error_response(message: str, status: int = 200):
    """Return a standard error JSON response."""
    return jsonify({"success": False, "message": message}), status


# ══════════════════════════════════════════════════════════════════════
# ROUTE 1:  GET  /health
# Quick check — is the server up?  Can it reach the database?
# ══════════════════════════════════════════════════════════════════════

@app.route('/health', methods=['GET'])
def health():
    """
    Returns the current health status of the API and the database.

    Response:
        {
            "success": true,
            "api":     "running",
            "db":      "connected"   |  "unreachable"
        }
    """
    conn = get_connection()
    db_status = "connected" if conn else "unreachable"
    if conn:
        conn.close()

    return success_response({"api": "running", "db": db_status})


# ══════════════════════════════════════════════════════════════════════
# ROUTE 2:  POST  /register
# Create a brand-new user account.
# ══════════════════════════════════════════════════════════════════════

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Request JSON:
        username  (str, required)  — unique login name
        email     (str, required)  — unique email address
        password  (str, required)  — plain-text; hashed by auth.py
        fullName  (str, optional)  — display name

    Response (success):
        { "success": true, "message": "✅ Account created! Welcome, <username>!" }

    Response (failure):
        { "success": false, "message": "<reason>" }
    """

    data = request.get_json(silent=True)

    # Guard: ensure the request body is valid JSON
    if not data:
        return error_response("Request body must be JSON.")

    # Extract fields
    username  = data.get('username',  '').strip()
    email     = data.get('email',     '').strip()
    password  = data.get('password',  '').strip()
    full_name = data.get('fullName',  '').strip()

    # ── Server-side validation ────────────────────────────────────────
    if not username or not email or not password:
        return error_response("Username, email and password are all required.")

    if len(username) < 3:
        return error_response("Username must be at least 3 characters.")

    if len(username) > 50:
        return error_response("Username must be 50 characters or fewer.")

    if not is_valid_email(email):
        return error_response("Please provide a valid email address.")

    if len(password) < 6:
        return error_response("Password must be at least 6 characters.")

    # ── Delegate to auth layer ────────────────────────────────────────
    ok, message = register_user(username, email, password, full_name)

    if ok:
        return success_response({"message": message})
    else:
        return error_response(message)


# ══════════════════════════════════════════════════════════════════════
# ROUTE 3:  POST  /login
# Authenticate a user and return their profile.
# ══════════════════════════════════════════════════════════════════════

@app.route('/login', methods=['POST'])
def login():
    """
    Log in an existing user.

    Request JSON:
        username  (str, required)
        password  (str, required)  — plain-text; compared to bcrypt hash

    Response (success):
        {
            "success": true,
            "user": {
                "id":         <int>,
                "username":   <str>,
                "email":      <str>,
                "full_name":  <str>,
                "created_at": <str>
            }
        }

    Response (failure):
        { "success": false, "message": "<reason>" }
    """

    data = request.get_json(silent=True)

    if not data:
        return error_response("Request body must be JSON.")

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return error_response("Username and password are required.")

    # ── Delegate to auth layer ────────────────────────────────────────
    ok, result = login_user(username, password)

    if ok:
        return success_response({"user": result})
    else:
        return error_response(result)


# ══════════════════════════════════════════════════════════════════════
# ROUTE 4:  GET  /user/<id>
# Fetch a single user's public profile by their numeric ID.
# ══════════════════════════════════════════════════════════════════════

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a user by ID.

    URL param:
        user_id  (int)  — the user's primary key

    Response (success):
        { "success": true, "user": { id, username, email, full_name, created_at } }

    Response (failure):
        { "success": false, "message": "User not found." }
    """

    conn = get_connection()
    if not conn:
        return error_response("Database connection failed.")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, email, full_name, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            return error_response("User not found.")

        # Convert datetime to string so it serialises cleanly
        if user.get('created_at'):
            user['created_at'] = str(user['created_at'])

        return success_response({"user": user})

    except Exception as e:
        return error_response(f"Error fetching user: {str(e)}")

    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()


# ══════════════════════════════════════════════════════════════════════
# ROUTE 5:  GET  /users
# Return a list of all users (for admin / debug purposes).
# Remove or protect this route before going to production.
# ══════════════════════════════════════════════════════════════════════

@app.route('/users', methods=['GET'])
def get_all_users():
    """
    List all users.

    Query params (optional):
        limit   (int, default=50)   — max rows to return
        offset  (int, default=0)    — pagination offset

    Response:
        { "success": true, "count": <int>, "users": [ {...}, ... ] }
    """

    # Parse optional pagination params
    try:
        limit  = int(request.args.get('limit',  50))
        offset = int(request.args.get('offset',  0))
    except ValueError:
        return error_response("limit and offset must be integers.")

    # Cap limit to prevent huge responses
    limit = min(limit, 200)

    conn = get_connection()
    if not conn:
        return error_response("Database connection failed.")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, email, full_name, created_at "
            "FROM users ORDER BY id ASC LIMIT %s OFFSET %s",
            (limit, offset)
        )
        users = cursor.fetchall()

        # Stringify datetime fields
        for u in users:
            if u.get('created_at'):
                u['created_at'] = str(u['created_at'])

        return success_response({"count": len(users), "users": users})

    except Exception as e:
        return error_response(f"Error fetching users: {str(e)}")

    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()


# ══════════════════════════════════════════════════════════════════════
# ROUTE 6:  PUT  /user/<id>
# Update a user's full_name and/or email.
# ══════════════════════════════════════════════════════════════════════

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user's profile fields.

    URL param:
        user_id  (int)

    Request JSON (at least one field required):
        fullName  (str, optional)  — new display name
        email     (str, optional)  — new email address

    Response:
        { "success": true, "message": "Profile updated successfully." }
    """

    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body must be JSON.")

    full_name = data.get('fullName', '').strip()
    email     = data.get('email',    '').strip()

    if not full_name and not email:
        return error_response("Provide at least one field to update: fullName or email.")

    if email and not is_valid_email(email):
        return error_response("Please provide a valid email address.")

    conn = get_connection()
    if not conn:
        return error_response("Database connection failed.")

    try:
        cursor = conn.cursor()

        # Build the SET clause dynamically based on what was provided
        fields, values = [], []
        if full_name:
            fields.append("full_name = %s")
            values.append(full_name)
        if email:
            fields.append("email = %s")
            values.append(email)

        values.append(user_id)   # for the WHERE clause

        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(sql, tuple(values))
        conn.commit()

        if cursor.rowcount == 0:
            return error_response("User not found.")

        return success_response({"message": "Profile updated successfully."})

    except Exception as e:
        error_msg = str(e)
        if "Duplicate" in error_msg:
            return error_response("That email address is already in use.")
        return error_response(f"Update failed: {error_msg}")

    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()


# ══════════════════════════════════════════════════════════════════════
# ROUTE 7:  DELETE  /user/<id>
# Permanently remove a user account.
# ══════════════════════════════════════════════════════════════════════

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID.

    URL param:
        user_id  (int)

    Response:
        { "success": true, "message": "User deleted successfully." }
    """

    conn = get_connection()
    if not conn:
        return error_response("Database connection failed.")

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return error_response("User not found.")

        return success_response({"message": "User deleted successfully."})

    except Exception as e:
        return error_response(f"Delete failed: {str(e)}")

    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()


# ══════════════════════════════════════════════════════════════════════
# 404 HANDLER  —  Unknown routes return clean JSON instead of HTML
# ══════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return error_response("Endpoint not found. Check the URL and method.", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return error_response("HTTP method not allowed for this endpoint.", 405)


# ══════════════════════════════════════════════════════════════════════
# START THE SERVER
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀  Flask API running  →  http://localhost:{port}")
    print("─" * 50)
    print("  GET   /health")
    print("  POST  /register")
    print("  POST  /login")
    print("  GET   /user/<id>")
    print("  GET   /users")
    print("  PUT   /user/<id>")
    print("  DELETE /user/<id>")
    print("─" * 50)
    app.run(host="0.0.0.0", port=port, debug=True)