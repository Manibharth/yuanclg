# ══════════════════════════════════════════════════════════
# main.py  →  Tkinter GUI Login & Register Form
# Run:  python main.py
# ══════════════════════════════════════════════════════════

# Step 1: Import tkinter — Python's built-in GUI library (no install needed)
import tkinter as tk
from tkinter import messagebox  # For popup dialogs (info, error, warning)
from tkinter import ttk         # ttk = themed Tkinter widgets (nicer looking)

# Step 2: Import our authentication functions
from auth import login_user, register_user


# ══════════════════════════════════════════════════════════
# CLASS: LoginApp
# Using a class keeps all GUI code organized in one place
# ══════════════════════════════════════════════════════════
class LoginApp:

    def __init__(self, root):
        """
        Constructor — runs when the object is created.
        Sets up the main window and shows the login frame.

        Parameter:
            root (Tk): The main Tkinter window object
        """

        # Step 3: Store the root window reference
        self.root = root

        # Step 4: Set the window title (shown in taskbar)
        self.root.title("🎓 Student Login Portal")

        # Step 5: Set the window size (width x height)
        self.root.geometry("480x580")

        # Step 6: Prevent window from being resized
        self.root.resizable(False, False)

        # Step 7: Set background color of the main window
        self.root.configure(bg="#0f0f1a")

        # Step 8: Center the window on the screen
        self.center_window(480, 580)

        # Step 9: Show the login screen first
        self.show_login_frame()


    # ─────────────────────────────────────────────
    # HELPER: Center the window on screen
    # ─────────────────────────────────────────────
    def center_window(self, width, height):
        """
        Positions the window in the center of the screen.
        """
        # Step 10: Get screen dimensions using winfo methods
        screen_w = self.root.winfo_screenwidth()   # Total screen width in pixels
        screen_h = self.root.winfo_screenheight()  # Total screen height in pixels

        # Step 11: Calculate top-left corner coordinates for centering
        x = (screen_w // 2) - (width  // 2)  # // = floor division (no decimals)
        y = (screen_h // 2) - (height // 2)

        # Step 12: Apply position using geometry string format: "WxH+X+Y"
        self.root.geometry(f"{width}x{height}+{x}+{y}")


    # ─────────────────────────────────────────────
    # HELPER: Clear all widgets from the window
    # ─────────────────────────────────────────────
    def clear_window(self):
        """
        Destroys all existing widgets in the root window.
        Called before switching between Login and Register screens.
        """
        # Step 13: Loop through every child widget and destroy it
        for widget in self.root.winfo_children():
            widget.destroy()


    # ─────────────────────────────────────────────
    # HELPER: Create a styled label
    # ─────────────────────────────────────────────
    def make_label(self, parent, text, size=12, color="#cccccc", bold=False):
        weight = "bold" if bold else "normal"
        return tk.Label(
            parent,
            text=text,
            font=("Consolas", size, weight),  # Monospace font for techy look
            fg=color,
            bg="#0f0f1a"
        )


    # ─────────────────────────────────────────────
    # HELPER: Create a styled Entry (text input)
    # ─────────────────────────────────────────────
    def make_entry(self, parent, show=None):
        """
        Creates a styled input field.
        show="*" makes the text appear as dots (for passwords).
        """
        entry = tk.Entry(
            parent,
            font=("Consolas", 12),
            bg="#1e1e2e",          # Dark background
            fg="#ffffff",          # White text
            insertbackground="#e94560",  # Cursor color
            relief="flat",         # No 3D border
            bd=8,                  # Padding inside the box
            show=show              # None = normal, "*" = password dots
        )
        # Bind hover effects
        entry.bind("<FocusIn>",  lambda e: entry.config(bg="#2a2a3e"))  # Lighten on focus
        entry.bind("<FocusOut>", lambda e: entry.config(bg="#1e1e2e"))  # Darken on blur
        return entry


    # ─────────────────────────────────────────────
    # HELPER: Create a styled Button
    # ─────────────────────────────────────────────
    def make_button(self, parent, text, command, color="#e94560"):
        btn = tk.Button(
            parent,
            text=text,
            command=command,         # Function to call when clicked
            font=("Consolas", 13, "bold"),
            bg=color,
            fg="white",
            activebackground="#c73652",   # Color when clicked
            activeforeground="white",
            relief="flat",
            cursor="hand2",              # Mouse turns into a pointer on hover
            bd=0,
            pady=10
        )
        return btn


    # ══════════════════════════════════════════════════════════
    # SCREEN 1: LOGIN FRAME
    # ══════════════════════════════════════════════════════════
    def show_login_frame(self):
        """
        Builds and displays the Login UI screen.
        """

        # Step 14: Clear any existing widgets first
        self.clear_window()

        # ── Header ──────────────────────────────
        # Step 15: Add a top banner frame
        header = tk.Frame(self.root, bg="#e94560", height=6)
        header.pack(fill="x")  # fill="x" → stretch full width

        # Step 16: Title label
        self.make_label(self.root, "🎓 Student Portal", size=22, color="#ffffff", bold=True)\
            .pack(pady=(40, 5))

        # Step 17: Subtitle
        self.make_label(self.root, "Sign in to your account", size=11, color="#888888")\
            .pack(pady=(0, 30))

        # ── Input container ─────────────────────
        # Step 18: A frame to hold the form fields (for clean layout)
        form = tk.Frame(self.root, bg="#0f0f1a")
        form.pack(padx=50, fill="x")

        # ── Username ────────────────────────────
        # Step 19: Username label
        self.make_label(form, "USERNAME", size=9, color="#e94560", bold=True).pack(anchor="w")

        # Step 20: Username entry field
        self.login_username = self.make_entry(form)
        self.login_username.pack(fill="x", pady=(4, 16), ipady=5)
        # self.login_username is stored as instance variable so we can read it later

        # ── Password ────────────────────────────
        # Step 21: Password label
        self.make_label(form, "PASSWORD", size=9, color="#e94560", bold=True).pack(anchor="w")

        # Step 22: Password entry field (show="*" hides characters)
        self.login_password = self.make_entry(form, show="*")
        self.login_password.pack(fill="x", pady=(4, 6), ipady=5)

        # ── Show/Hide password checkbox ─────────
        # Step 23: Variable to track checkbox state (0=off, 1=on)
        self.show_pw_var = tk.IntVar()
        show_cb = tk.Checkbutton(
            form,
            text=" Show Password",
            variable=self.show_pw_var,
            command=self.toggle_login_password,  # Called when checkbox is toggled
            font=("Consolas", 10),
            fg="#888888",
            bg="#0f0f1a",
            selectcolor="#1e1e2e",
            activebackground="#0f0f1a",
            activeforeground="#cccccc",
            cursor="hand2"
        )
        show_cb.pack(anchor="w", pady=(0, 25))

        # ── Login Button ─────────────────────────
        # Step 24: Login button — calls handle_login when clicked
        self.make_button(form, "  LOGIN  →  ", self.handle_login)\
            .pack(fill="x", pady=(0, 20))

        # ── Separator ────────────────────────────
        # Step 25: A horizontal line to separate sections
        tk.Frame(form, bg="#2a2a3e", height=1).pack(fill="x", pady=10)

        # ── Register link ────────────────────────
        # Step 26: Row frame to put text and button side by side
        row = tk.Frame(form, bg="#0f0f1a")
        row.pack()

        self.make_label(row, "No account?", size=10, color="#888888").pack(side="left")

        # Step 27: A text-style button for switching to Register screen
        tk.Button(
            row,
            text=" Register here",
            command=self.show_register_frame,  # Switch to register screen
            font=("Consolas", 10, "underline"),
            fg="#e94560",
            bg="#0f0f1a",
            relief="flat",
            bd=0,
            cursor="hand2",
            activeforeground="#c73652",
            activebackground="#0f0f1a"
        ).pack(side="left")

        # Step 28: Set focus to username field so user can type immediately
        self.login_username.focus()

        # Step 29: Bind Enter key to trigger login
        self.root.bind("<Return>", lambda e: self.handle_login())


    # ─────────────────────────────────────────────
    # Toggle password visibility on login screen
    # ─────────────────────────────────────────────
    def toggle_login_password(self):
        """
        Called when Show Password checkbox is toggled.
        show="" → show characters | show="*" → hide characters
        """
        # Step 30: If checked (1), show password; if unchecked (0), hide it
        if self.show_pw_var.get() == 1:
            self.login_password.config(show="")   # Show characters
        else:
            self.login_password.config(show="*")  # Hide characters


    # ─────────────────────────────────────────────
    # Handle Login button click
    # ─────────────────────────────────────────────
    def handle_login(self):
        """
        Reads the entered username and password,
        calls login_user() from auth.py, and handles the result.
        """

        # Step 31: Read values from entry fields using .get()
        #          .strip() removes accidental spaces before/after
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        # Step 32: Show a loading/processing state (update button text)
        # (Optional — useful for slow connections)

        # Step 33: Call the login function from auth.py
        success, result = login_user(username, password)

        if success:
            # Step 34: Login worked — 'result' is the user dict
            self.show_dashboard(result)  # Go to dashboard screen

        else:
            # Step 35: Login failed — 'result' is the error string
            # showerror() shows a popup dialog with red X icon
            messagebox.showerror("Login Failed", result)


    # ══════════════════════════════════════════════════════════
    # SCREEN 2: REGISTER FRAME
    # ══════════════════════════════════════════════════════════
    def show_register_frame(self):
        """
        Builds and displays the Registration UI screen.
        """

        # Step 36: Clear window and rebuild
        self.clear_window()

        # ── Header ──────────────────────────────
        tk.Frame(self.root, bg="#4ecca3", height=6).pack(fill="x")

        self.make_label(self.root, "📝 Create Account", size=20, color="#ffffff", bold=True)\
            .pack(pady=(30, 5))

        self.make_label(self.root, "Fill in your details below", size=11, color="#888888")\
            .pack(pady=(0, 20))

        # ── Form frame ──────────────────────────
        form = tk.Frame(self.root, bg="#0f0f1a")
        form.pack(padx=50, fill="x")

        # ── Full Name ───────────────────────────
        # Step 37: Full name field (optional)
        self.make_label(form, "FULL NAME", size=9, color="#4ecca3", bold=True).pack(anchor="w")
        self.reg_fullname = self.make_entry(form)
        self.reg_fullname.pack(fill="x", pady=(4, 12), ipady=5)

        # ── Username ─────────────────────────────
        self.make_label(form, "USERNAME *", size=9, color="#4ecca3", bold=True).pack(anchor="w")
        self.reg_username = self.make_entry(form)
        self.reg_username.pack(fill="x", pady=(4, 12), ipady=5)

        # ── Email ────────────────────────────────
        self.make_label(form, "EMAIL *", size=9, color="#4ecca3", bold=True).pack(anchor="w")
        self.reg_email = self.make_entry(form)
        self.reg_email.pack(fill="x", pady=(4, 12), ipady=5)

        # ── Password ─────────────────────────────
        self.make_label(form, "PASSWORD *", size=9, color="#4ecca3", bold=True).pack(anchor="w")
        self.reg_password = self.make_entry(form, show="*")
        self.reg_password.pack(fill="x", pady=(4, 20), ipady=5)

        # ── Register Button ───────────────────────
        # Step 38: Register button — calls handle_register
        self.make_button(form, "  CREATE ACCOUNT  ", self.handle_register, color="#4ecca3")\
            .pack(fill="x", pady=(0, 15))

        # ── Back to Login ─────────────────────────
        tk.Frame(form, bg="#2a2a3e", height=1).pack(fill="x", pady=8)

        row = tk.Frame(form, bg="#0f0f1a")
        row.pack()
        self.make_label(row, "Already registered?", size=10, color="#888888").pack(side="left")
        tk.Button(
            row, text=" Login here",
            command=self.show_login_frame,
            font=("Consolas", 10, "underline"),
            fg="#4ecca3", bg="#0f0f1a", relief="flat",
            bd=0, cursor="hand2",
            activeforeground="#3ab88a", activebackground="#0f0f1a"
        ).pack(side="left")

        # Step 39: Focus on first field
        self.reg_fullname.focus()
        self.root.bind("<Return>", lambda e: self.handle_register())


    # ─────────────────────────────────────────────
    # Handle Register button click
    # ─────────────────────────────────────────────
    def handle_register(self):
        """
        Reads registration fields and calls register_user() from auth.py.
        """

        # Step 40: Read all field values
        full_name = self.reg_fullname.get().strip()
        username  = self.reg_username.get().strip()
        email     = self.reg_email.get().strip()
        password  = self.reg_password.get().strip()

        # Step 41: Call register_user() from auth.py
        success, message = register_user(username, email, password, full_name)

        if success:
            # Step 42: Show success popup and go back to login
            messagebox.showinfo("Registered!", message)
            self.show_login_frame()
        else:
            # Step 43: Show error popup
            messagebox.showerror("Registration Failed", message)


    # ══════════════════════════════════════════════════════════
    # SCREEN 3: DASHBOARD (after successful login)
    # ══════════════════════════════════════════════════════════
    def show_dashboard(self, user):
        """
        Shows a welcome dashboard after login.
        Parameter:
            user (dict): The logged-in user's data from the database
        """

        # Step 44: Clear and rebuild window
        self.clear_window()
        self.root.geometry("480x420")

        # ── Green top bar ───────────────────────
        tk.Frame(self.root, bg="#4ecca3", height=6).pack(fill="x")

        # Step 45: Show welcome message using the user's username from DB
        self.make_label(
            self.root,
            f"✅  Welcome, {user.get('username', 'Student')}!",
            size=20, color="#4ecca3", bold=True
        ).pack(pady=(40, 10))

        self.make_label(self.root, "You are successfully logged in.", size=11, color="#aaaaaa")\
            .pack()

        # ── User Info Card ───────────────────────
        # Step 46: Frame to display user info
        card = tk.Frame(self.root, bg="#1e1e2e", padx=20, pady=20)
        card.pack(padx=50, pady=30, fill="x")

        # Step 47: Display each user field from the database result
        fields = [
            ("👤  ID",         str(user.get('id', '-'))),
            ("📛  Full Name",  user.get('full_name', '-') or '-'),
            ("🏷️  Username",  user.get('username',  '-')),
            ("📧  Email",      user.get('email',     '-')),
            ("📅  Joined",     str(user.get('created_at', '-'))),
        ]

        for label_text, value_text in fields:
            # Step 48: Each row is a sub-frame with label on left, value on right
            row = tk.Frame(card, bg="#1e1e2e")
            row.pack(fill="x", pady=4)

            tk.Label(row, text=label_text, font=("Consolas", 10),
                     fg="#888888", bg="#1e1e2e", width=18, anchor="w")\
                .pack(side="left")

            tk.Label(row, text=value_text, font=("Consolas", 10, "bold"),
                     fg="#ffffff", bg="#1e1e2e")\
                .pack(side="left")

        # ── Logout Button ────────────────────────
        # Step 49: Logout goes back to the login screen
        self.make_button(self.root, "  LOGOUT  ", self.show_login_frame, color="#444455")\
            .pack(pady=10, padx=50, fill="x")


# ══════════════════════════════════════════════════════════
# ENTRY POINT — Runs when you execute:  python main.py
# ══════════════════════════════════════════════════════════

# Step 50: Only run if this file is executed directly (not imported)
if __name__ == "__main__":

    # Step 51: Create the main Tkinter window (root)
    root = tk.Tk()

    # Step 52: Create the LoginApp object, passing the root window
    app = LoginApp(root)

    # Step 53: Start the Tkinter event loop
    #          mainloop() keeps the window open and listens for events (clicks, keypresses)
    #          The program runs until the window is closed
    root.mainloop()