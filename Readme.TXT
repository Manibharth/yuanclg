# ══════════════════════════════════════════════════════════
# README  →  How to run this project
# ══════════════════════════════════════════════════════════

📁 FILES IN THIS PROJECT:
─────────────────────────────────────────
  setup.sql      →  Run this in MySQL FIRST
  db_config.py   →  DB credentials & connection
  auth.py        →  Login & Register logic
  main.py        →  GUI Login Form (run this!)

══════════════════════════════════════════
STEP 1: Install required libraries
══════════════════════════════════════════
Open terminal/CMD and run:

    pip install mysql-connector-python bcrypt

══════════════════════════════════════════
STEP 2: Set up MySQL Database
══════════════════════════════════════════
1. Open phpMyAdmin or MySQL Workbench
2. Open setup.sql
3. Run/Execute it
4. This creates: student_login_db → users table

══════════════════════════════════════════
STEP 3: Configure db_config.py
══════════════════════════════════════════
Open db_config.py and change:
    "user":     "root"       ← your MySQL username
    "password": "yuan@123"           ← your MySQL password

══════════════════════════════════════════
STEP 4: Run the app
══════════════════════════════════════════
    python main.py

══════════════════════════════════════════
TEST CREDENTIALS (from setup.sql):
══════════════════════════════════════════
    Username : root
    Password : yuan@123

    (Or click "Register here" to create a new account)