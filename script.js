/* ═══════════════════════════════════════════════════════
   script.js  —  Student Login Portal
   Now connects to Flask API → MySQL (no more fake array!)
   ═══════════════════════════════════════════════════════ */


/* ───────────────────────────────────────────────────────
   SECTION 1: API BASE URL
   All fetch() calls will go to our Flask server
─────────────────────────────────────────────────────── */

// Step 1: Flask server address — must match server.py port
// ✅ Replace with your actual Railway URL
const API_URL = "https://manibharth.github.io/yuanclg/";

// Tracks the currently logged-in user object
let currentUser = null;


/* ───────────────────────────────────────────────────────
   SECTION 2: PAGE SWITCHING
─────────────────────────────────────────────────────── */

function showPage(name) {
  const allPages = document.querySelectorAll(".page");
  allPages.forEach(function(page) {
    page.classList.remove("active");
  });
  const target = document.getElementById("page-" + name);
  if (target) {
    target.classList.add("active");
  }
  clearAlerts();
}


/* ───────────────────────────────────────────────────────
   SECTION 3: ALERT HELPERS
─────────────────────────────────────────────────────── */

function showAlert(id, message) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = message;
  el.style.display = "block";
}

function hideAlert(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.display = "none";
  el.textContent = "";
}

function clearAlerts() {
  ["login-error", "reg-error", "reg-success"].forEach(function(id) {
    hideAlert(id);
  });
}


/* ───────────────────────────────────────────────────────
   SECTION 4: SHOW / HIDE PASSWORD
─────────────────────────────────────────────────────── */

const showPwCheckbox = document.getElementById("show-pw-cb");
const loginPassInput = document.getElementById("l-pass");

if (showPwCheckbox) {
  showPwCheckbox.addEventListener("change", function() {
    loginPassInput.type = showPwCheckbox.checked ? "text" : "password";
  });
}


/* ───────────────────────────────────────────────────────
   SECTION 5: HANDLE LOGIN FORM SUBMIT
   Now sends fetch() POST to Flask /login
─────────────────────────────────────────────────────── */

const loginForm = document.getElementById("login-form");

if (loginForm) {
  loginForm.addEventListener("submit", async function(event) {

    // Step 1: Stop page reload
    event.preventDefault();

    // Step 2: Read inputs
    const username = document.getElementById("l-user").value.trim();
    const password = document.getElementById("l-pass").value.trim();

    // Step 3: Basic validation
    if (!username || !password) {
      showAlert("login-error", "Please fill in all fields.");
      return;
    }

    try {
      // Step 4: Send POST request to Flask /login with JSON body
      const response = await fetch(API_URL + "/login", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ username, password })
      });

      // Step 5: Parse the JSON response from Flask
      const data = await response.json();

      // Step 6a: Login failed → show error message
      if (!data.success) {
        showAlert("login-error", data.message);
        return;
      }

      // Step 6b: Login success → go to dashboard
      currentUser = data.user;
      updateDashboard(data.user);
      showPage("dashboard");

    } catch (err) {
      // Step 7: Network error (Flask server not running?)
      showAlert("login-error", "❌ Cannot connect to server. Is Flask running?");
    }
  });
}


/* ───────────────────────────────────────────────────────
   SECTION 6: HANDLE REGISTER FORM SUBMIT
   Now sends fetch() POST to Flask /register
─────────────────────────────────────────────────────── */

const registerForm = document.getElementById("register-form");

if (registerForm) {
  registerForm.addEventListener("submit", async function(event) {

    // Step 1: Stop page reload
    event.preventDefault();

    // Step 2: Read all field values
    const fullName = document.getElementById("r-name").value.trim();
    const username = document.getElementById("r-user").value.trim();
    const email    = document.getElementById("r-email").value.trim();
    const password = document.getElementById("r-pass").value.trim();

    // Step 3: Hide old alerts
    hideAlert("reg-error");
    hideAlert("reg-success");

    // Step 4: Validate required fields
    if (!username || !email || !password) {
      showAlert("reg-error", "Username, Email and Password are required.");
      return;
    }

    // Step 5: Validate password length
    if (password.length < 6) {
      showAlert("reg-error", "Password must be at least 6 characters.");
      return;
    }

    // Step 6: Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      showAlert("reg-error", "Please enter a valid email address.");
      return;
    }

    try {
      // Step 7: Send POST request to Flask /register with JSON body
      const response = await fetch(API_URL + "/register", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ username, email, password, fullName })
      });

      // Step 8: Parse the JSON response
      const data = await response.json();

      // Step 9a: Registration failed (duplicate user, etc.)
      if (!data.success) {
        showAlert("reg-error", data.message);
        return;
      }

      // Step 9b: Success! Show message and redirect to login after 1.2s
      showAlert("reg-success", data.message);
      registerForm.reset();

      setTimeout(function() {
        showPage("login");
      }, 1200);

    } catch (err) {
      // Step 10: Network error
      showAlert("reg-error", "❌ Cannot connect to server. Is Flask running?");
    }
  });
}


/* ───────────────────────────────────────────────────────
   SECTION 7: POPULATE DASHBOARD WITH USER DATA
─────────────────────────────────────────────────────── */

function updateDashboard(user) {

  // Step 1: Avatar = first 2 letters of username
  const avatarEl = document.getElementById("dash-avatar");
  if (avatarEl) {
    avatarEl.textContent = user.username.slice(0, 2).toUpperCase();
  }

  // Step 2: Welcome heading
  const welcomeEl = document.getElementById("dash-welcome");
  if (welcomeEl) {
    welcomeEl.textContent = "Welcome, " + user.username + "!";
  }

  // Step 3: Fill info rows
  //         'id' and 'full_name' match the column names returned by auth.py
  document.getElementById("d-id").textContent    = "#" + user.id;
  document.getElementById("d-name").textContent  = user.full_name || "Not provided";
  document.getElementById("d-user").textContent  = user.username;
  document.getElementById("d-email").textContent = user.email;
}


/* ───────────────────────────────────────────────────────
   SECTION 8: LOGOUT
─────────────────────────────────────────────────────── */

const logoutBtn = document.getElementById("logout-btn");

if (logoutBtn) {
  logoutBtn.addEventListener("click", function() {

    // Step 1: Clear current user
    currentUser = null;

    // Step 2: Reset login form
    const loginFormEl = document.getElementById("login-form");
    if (loginFormEl) loginFormEl.reset();

    // Step 3: Go back to login page
    showPage("login");
  });
}


/* ───────────────────────────────────────────────────────
   SECTION 9: DATA-GOTO BUTTONS
─────────────────────────────────────────────────────── */

const gotoButtons = document.querySelectorAll("[data-goto]");

gotoButtons.forEach(function(btn) {
  btn.addEventListener("click", function() {
    const target = btn.getAttribute("data-goto");
    showPage(target);
  });
});


/* ───────────────────────────────────────────────────────
   SECTION 10: ENTER KEY SUPPORT
─────────────────────────────────────────────────────── */

document.addEventListener("keydown", function(event) {
  if (event.key !== "Enter") return;

  const activePage = document.querySelector(".page.active");
  if (!activePage) return;

  const pageId = activePage.id;

  if (pageId === "page-login") {
    loginForm.dispatchEvent(new Event("submit"));
  } else if (pageId === "page-register") {
    registerForm.dispatchEvent(new Event("submit"));
  }
});