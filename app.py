from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import secrets
import string
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ---------------------------------------------------------
# DATABASE CONFIG — edit these to match your local MySQL setup
# ---------------------------------------------------------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ---------------------------------------------------------
# Simple keyword-based flagging.
# This is NOT a crisis-detection system — it's a basic safety
# net so urgent-sounding messages get a staff member's eyes
# faster instead of sitting in a queue. Always say this out
# loud in the demo: it's an on-ramp, not a diagnosis.
# ---------------------------------------------------------
FLAG_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "hurt myself",
    "want to die", "can't take this anymore", "no reason to live",
    "hopeless", "give up on life"
]

def is_flagged(text):
    t = text.lower()
    return any(k in t for k in FLAG_KEYWORDS)

def generate_passcode():
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))

# ---------------------------------------------------------
# Student-facing routes
# ---------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    mode = request.form.get('mode', 'vent')
    message = request.form.get('message', '').strip()
    name = request.form.get('name') or None
    branch = request.form.get('branch') or None
    year = request.form.get('year') or None
    hostel_block = request.form.get('hostel_block') or None

    if not message:
        flash("Please describe what's happening before submitting.")
        return redirect(url_for('index'))

    flagged = is_flagged(message)
    passcode = generate_passcode()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reports (passcode, mode, message, name, branch, year, hostel_block, flagged)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (passcode, mode, message, name, branch, year, hostel_block, flagged))
    conn.commit()
    cur.close()
    conn.close()

    return render_template('passcode_result.html', passcode=passcode)

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        code = request.form.get('passcode', '').strip().upper()
        return redirect(url_for('thread', passcode=code))
    return render_template('check.html')

@app.route('/thread/<passcode>', methods=['GET', 'POST'])
def thread(passcode):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM reports WHERE passcode=%s", (passcode,))
    report = cur.fetchone()

    if not report:
        cur.close()
        conn.close()
        flash("That passcode doesn't match any report. Double-check it.")
        return redirect(url_for('check'))

    if request.method == 'POST':
        reply_msg = request.form.get('message', '').strip()
        if reply_msg:
            cur.execute(
                "INSERT INTO replies (report_id, sender, message) VALUES (%s,'student',%s)",
                (report['id'], reply_msg)
            )
            conn.commit()

    cur.execute("SELECT * FROM replies WHERE report_id=%s ORDER BY created_at ASC", (report['id'],))
    replies = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('thread.html', report=report, replies=replies)

# ---------------------------------------------------------
# Staff-facing routes (counselor / warden side)
# ---------------------------------------------------------

STAFF_PASSWORD = os.getenv("STAFF_PASSWORD")  # demo-only, hardcoded on purpose for the prototype

def require_staff():
    return session.get('staff', False)

@app.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        pw = request.form.get('password')
        if pw == STAFF_PASSWORD:
            session['staff'] = True
            return redirect(url_for('dashboard'))
        flash("Incorrect password.")
    return render_template('staff_login.html')

@app.route('/staff/logout')
def staff_logout():
    session.pop('staff', None)
    return redirect(url_for('index'))

@app.route('/staff/dashboard')
def dashboard():
    if not require_staff():
        return redirect(url_for('staff_login'))
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM reports ORDER BY flagged DESC, created_at DESC")
    reports = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('dashboard.html', reports=reports)

@app.route('/staff/report/<int:report_id>', methods=['GET', 'POST'])
def report_detail(report_id):
    if not require_staff():
        return redirect(url_for('staff_login'))
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    if request.method == 'POST':
        reply_msg = request.form.get('message', '').strip()
        new_status = request.form.get('status')
        if reply_msg:
            cur.execute(
                "INSERT INTO replies (report_id, sender, message) VALUES (%s,'staff',%s)",
                (report_id, reply_msg)
            )
        if new_status:
            cur.execute("UPDATE reports SET status=%s WHERE id=%s", (new_status, report_id))
        conn.commit()

    cur.execute("SELECT * FROM reports WHERE id=%s", (report_id,))
    report = cur.fetchone()
    cur.execute("SELECT * FROM replies WHERE report_id=%s ORDER BY created_at ASC", (report_id,))
    replies = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('report_detail.html', report=report, replies=replies)

if __name__ == '__main__':
    app.run(debug=True)
