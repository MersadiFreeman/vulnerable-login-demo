import os
import sqlite3
import time
from flask import Flask, request, render_template_string, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

# naive in-memory rate limit: {ip: [timestamps]}
attempts = {}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    conn.commit()

    # seed a demo user if missing
    cur = conn.execute("SELECT 1 FROM users WHERE username = ?", ("admin",))
    if not cur.fetchone():
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", generate_password_hash("password123")),
        )
        conn.commit()

    conn.close()


def too_many_attempts(ip: str, limit: int = 5, window_seconds: int = 60) -> bool:
    now = time.time()
    recent = [t for t in attempts.get(ip, []) if now - t < window_seconds]
    attempts[ip] = recent
    return len(recent) >= limit


def record_attempt(ip: str, window_seconds: int = 60) -> None:
    now = time.time()
    recent = [t for t in attempts.get(ip, []) if now - t < window_seconds]
    recent.append(now)
    attempts[ip] = recent


PAGE = """
<h2>Secure Login</h2>

{% if session.get("user") %}
  <p><b>Logged in as:</b> {{ session["user"] }}</p>
  <form method="POST" action="{{ url_for('logout') }}">
    <button type="submit">Logout</button>
  </form>
  <hr>
{% endif %}

<h3>Register</h3>
<form method="POST" action="{{ url_for('register') }}">
  Username: <input name="username" autocomplete="username"><br>
  Password: <input name="password" type="password" autocomplete="new-password"><br><br>
  <button type="submit">Create account</button>
</form>

<hr>

<h3>Login</h3>
<form method="POST" action="{{ url_for('login') }}">
  Username: <input name="username" autocomplete="username"><br>
  Password: <input name="password" type="password" autocomplete="current-password"><br><br>
  <button type="submit">Login</button>
</form>

<p style="color:red;">{{ message }}</p>
<p style="color:gray; font-size: 0.9em;">
  Notes: Passwords are hashed. Queries are parameterized. Basic rate-limiting is enabled.
</p>
"""


@app.route("/")
def index():
    return render_template_string(PAGE, message="")


@app.route("/register", methods=["POST"])
def register():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    if not username or not password:
        return render_template_string(PAGE, message="Username and password required.")

    pw_hash = generate_password_hash(password)

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, pw_hash),
        )
        conn.commit()
        return render_template_string(PAGE, message="Account created. Now log in.")
    except sqlite3.IntegrityError:
        return render_template_string(PAGE, message="That username is taken.")
    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    ip = request.remote_addr or "unknown"

    if too_many_attempts(ip):
        return render_template_string(PAGE, message="Too many attempts. Try again soon.")

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    record_attempt(ip)

    conn = get_db()
    try:
        cur = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
    finally:
        conn.close()

    if user and check_password_hash(user["password_hash"], password):
        session["user"] = user["username"]
        attempts.pop(ip, None)  # reset attempts on success
        return redirect(url_for("index"))

    return render_template_string(PAGE, message="Invalid username or password.")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
