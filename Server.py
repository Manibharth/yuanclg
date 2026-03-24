from flask import Flask, request, jsonify
from flask_cors import CORS

# Step 1: Import our auth functions
from auth import register_user, login_user

# Step 2: Create the Flask app
app = Flask(__name__)

# Step 3: Allow browser (Chrome) to talk to this server
#         Without CORS, browser blocks requests from index.html to Flask
CORS(app)


# ══════════════════════════════════════════════════════════
# ROUTE 1: POST /register
# Called by script.js when user submits the register form
# ══════════════════════════════════════════════════════════
@app.route('/register', methods=['POST'])
def register():

    # Step 4: Read JSON data sent from the browser
    data = request.get_json()

    # Step 5: Extract each field from the JSON
    username  = data.get('username', '')
    email     = data.get('email', '')
    password  = data.get('password', '')
    full_name = data.get('fullName', '')

    # Step 6: Call our register_user function from auth.py
    success, message = register_user(username, email, password, full_name)

    # Step 7: Return result as JSON back to the browser
    return jsonify({ "success": success, "message": message })


# ══════════════════════════════════════════════════════════
# ROUTE 2: POST /login
# Called by script.js when user submits the login form
# ══════════════════════════════════════════════════════════
@app.route('/login', methods=['POST'])
def login():

    # Step 8: Read JSON data sent from the browser
    data = request.get_json()

    username = data.get('username', '')
    password = data.get('password', '')

    # Step 9: Call our login_user function from auth.py
    success, result = login_user(username, password)

    # Step 10: If success, result is a user dict; if fail, it's an error string
    if success:
        return jsonify({ "success": True,  "user": result })
    else:
        return jsonify({ "success": False, "message": result })


# ══════════════════════════════════════════════════════════
# START THE SERVER
# ══════════════════════════════════════════════════════════
if __name__ == '__main__':
    # debug=True → auto-restarts server when you save changes
    # port=5000  → browser will call http://localhost:5000
    print("🚀 Flask server running at http://localhost:5000")
    app.run(debug=True, port=5000)