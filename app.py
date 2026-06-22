"""
DVWA-Style Brute Force Lab — Flask Backend
==========================================
INTENTIONALLY VULNERABLE — For cybersecurity education only.

Vulnerabilities implemented:
  - Login via HTTP GET (credentials in URL / server logs)
  - No rate limiting
  - No account lockout
  - No CSRF protection
  - Verbose error messages (username vs password distinction possible)
  - Plaintext password storage in memory (no hashing)
  - Session fixation possible (session not rotated on login)
"""

from flask import Flask, request, render_template, session, redirect, url_for, jsonify
import os
import datetime
import json

app = Flask(__name__)
# Weak secret key — intentionally predictable
app.secret_key = "dvwa_secret_key_123"
port = int(os.environ.get("PORT", 5000))

# ── In-memory "database" of users ─────────────────────────────────────────────
# Plaintext passwords — intentional vulnerability
USERS = {
    "admin":   {"password": "password",  "role": "Administrator", "flag": "FLAG{br3ak_th3_h@sh_&_st3al_th3_s3ss10n}"},
    "gordonb": {"password": "abc123",    "role": "User",          "flag": "FLAG{g0rd0n_b_w4s_h3r3}"},
    "1337":    {"password": "charley",   "role": "User",          "flag": "FLAG{1337_h4x0r_unl0ck3d}"},
    "pablo":   {"password": "letmein",   "role": "User",          "flag": "FLAG{p4bl0_3sc0b4r_l0g1n}"},
    "smithy":  {"password": "password",  "role": "User",          "flag": "FLAG{sm1thy_sm1th_sm1th}"},
}

# ── Attack log (in-memory, resets on container restart) ───────────────────────
attack_log = []

def log_attempt(username, password, success, ip):
    attempt = {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "username": username,
        "password": password,       # Logged in plaintext — intentional vulnerability
        "success": success,
    }
    attack_log.append(attempt)
    # Keep last 500 entries
    if len(attack_log) > 500:
        attack_log.pop(0)

# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("brute_force"))


@app.route("/login", methods=["GET"])
def login():
    return redirect(url_for("brute_force"))


@app.route("/vulnerabilities/brute/", methods=["GET"])
def brute_force():
    """
    VULNERABLE LOGIN ENDPOINT
    - Accepts credentials via GET parameters
    - No rate limiting
    - No lockout
    - No CSRF token
    """
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    result = None
    error = None
    user_data = None

    if request.args:  # Form was submitted
        ip = request.remote_addr
        user = USERS.get(username)

        if user and user["password"] == password:
            # ── Successful login ──────────────────────────────────────────────
            # No session.clear() before login — session fixation possible
            session["logged_in"] = True
            session["username"] = username
            session["role"] = user["role"]
            log_attempt(username, password, True, ip)
            user_data = {
                "username": username,
                "role": user["role"],
                "flag": user["flag"],
            }
            result = "success"
        else:
            # ── Failed login — constant error (no username enumeration) ───────
            log_attempt(username, password, False, ip)
            error = "Username or Password incorrect."
            result = "failure"

    return render_template(
        "brute.html",
        result=result,
        error=error,
        user_data=user_data,
        username=username,
        password=password,
        full_url=request.url,
        security_level="Low",
        logged_in=session.get("logged_in", False),
        session_user=session.get("username", ""),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("brute_force"))


@app.route("/attack-log")
def view_attack_log():
    """Exposes the full attack log — intentional information disclosure."""
    return render_template("attack_log.html", logs=attack_log, security_level="Low")


@app.route("/api/log")
def api_log():
    """JSON endpoint for the attack log — useful for automated tools."""
    return jsonify(attack_log)


@app.route("/api/reset-log", methods=["POST"])
def reset_log():
    attack_log.clear()
    return jsonify({"status": "ok", "message": "Attack log cleared."})


@app.route("/setup")
def setup():
    return render_template("setup.html", users=USERS, security_level="Low")


if __name__ == "__main__":
    # Debug mode on — intentional vulnerability (stack traces exposed)
    app.run(host="0.0.0.0", port=port, debug=True)
