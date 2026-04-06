"""
Fixed Web Application — Solutions for Workshop Exercise
Each fix is annotated with the vulnerability it addresses.
"""

import os
import sqlite3
import html
import subprocess
from pathlib import Path

import bcrypt
from flask import Flask, request, jsonify, session
from functools import wraps

app = Flask(__name__)

# FIX 1: Use environment variables instead of hardcoded credentials
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32).hex())
DB_PASSWORD = os.environ.get("DB_PASSWORD")
API_KEY = os.environ.get("API_KEY")


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


# FIX: Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        if session.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index():
    return jsonify({"status": "running"})


# FIX 3: Parameterized query prevents SQL injection
@app.route("/api/users")
@login_required
def get_users():
    username = request.args.get("username", "")
    conn = get_db()
    cursor = conn.execute(
        "SELECT id, username, email FROM users WHERE username = ?",
        (username,),
    )
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)


# FIX 4: Parameterized query + bcrypt password verification
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    # Input validation
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if len(username) > 100 or len(password) > 200:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db()
    cursor = conn.execute(
        "SELECT id, username, password, role FROM users WHERE username = ?",
        (username,),
    )
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        return jsonify({"message": "Login successful"})

    # Generic error message — don't reveal if user exists
    return jsonify({"error": "Invalid credentials"}), 401


# FIX 5: HTML escaping prevents XSS
@app.route("/search")
def search():
    q = request.args.get("q", "")
    # Escape user input before rendering
    safe_q = html.escape(q)
    return f"""
    <html><body>
        <h1>Search Results</h1>
        <p>You searched for: {safe_q}</p>
        <p>No results found.</p>
    </body></html>
    """


# FIX 6: Input validation + subprocess with list args prevents command injection
@app.route("/api/ping")
@login_required
def ping():
    host = request.args.get("host", "")

    # Validate: only allow hostname/IP characters
    import re
    if not re.match(r'^[a-zA-Z0-9.\-]+$', host) or len(host) > 255:
        return jsonify({"error": "Invalid hostname"}), 400

    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "3", host],
            capture_output=True, text=True, timeout=5,
        )
        return jsonify({"output": result.stdout})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout"}), 408


# FIX 7: Path traversal prevention with resolve() check
@app.route("/api/files")
@login_required
def get_file():
    filename = request.args.get("name", "")
    if not filename:
        return jsonify({"error": "Filename required"}), 400

    base_dir = Path("/app/uploads").resolve()
    filepath = (base_dir / filename).resolve()

    # Ensure resolved path is still under base directory
    if not str(filepath).startswith(str(base_dir)):
        return jsonify({"error": "Access denied"}), 403

    try:
        content = filepath.read_text()
        return jsonify({"content": content})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


# FIX 8: bcrypt for password hashing + input validation
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()

    # Input validation
    if not username or not password or not email:
        return jsonify({"error": "All fields required"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if len(username) > 50 or len(email) > 100:
        return jsonify({"error": "Input too long"}), 400

    # Strong password hashing with bcrypt
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()

    return jsonify({"message": "User created"}), 201


# FIX 9: Authorization check on admin endpoints
@app.route("/api/admin/users")
@admin_required
def admin_users():
    conn = get_db()
    cursor = conn.execute("SELECT id, username, email, role FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)


@app.route("/api/admin/delete/<int:user_id>", methods=["DELETE"])
@admin_required
def admin_delete_user(user_id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted"})


# FIX 10: Generic error messages, no internal info exposure
@app.route("/api/debug")
@admin_required
def debug():
    return jsonify({"status": "ok"})


# FIX 11: SSRF prevention with URL allowlist
@app.route("/api/fetch")
@login_required
def fetch_url():
    import requests
    from urllib.parse import urlparse

    url = request.args.get("url", "")

    # Allowlist domains
    allowed_domains = {"api.example.com", "cdn.example.com"}
    parsed = urlparse(url)

    if parsed.hostname not in allowed_domains:
        return jsonify({"error": "Domain not allowed"}), 403
    if parsed.scheme not in ("http", "https"):
        return jsonify({"error": "Invalid scheme"}), 400

    try:
        resp = requests.get(url, timeout=5)
        return jsonify({"status": resp.status_code, "body": resp.text[:1000]})
    except Exception:
        return jsonify({"error": "Request failed"}), 400


# FIX 12: Use JSON instead of pickle for data import
@app.route("/api/import", methods=["POST"])
@login_required
def import_data():
    import json

    data = request.get_json()
    if not data or "payload" not in data:
        return jsonify({"error": "Invalid request"}), 400

    # Safe: parse as JSON instead of pickle
    try:
        obj = json.loads(data["payload"])
        return jsonify({"imported": obj})
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON payload"}), 400


if __name__ == "__main__":
    # FIX: debug=False in production
    app.run(host="0.0.0.0", port=5000, debug=False)
