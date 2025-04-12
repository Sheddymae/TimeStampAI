from flask import Flask, render_template, request
import sqlite3
import time
from face_detector import detect_face

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('timestamps.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS timestamps
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  type TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('timestamps.db')
    c = conn.cursor()
    c.execute("SELECT * FROM timestamps ORDER BY timestamp DESC")
    timestamps = c.fetchall()
    conn.close()
    return render_template('index.html', timestamps=timestamps)

@app.route('/detect', methods=['POST'])
def detect():
    action = request.form['action']
    timestamp = detect_face()
    if timestamp:
        conn = sqlite3.connect('timestamps.db')
        c = conn.cursor()
        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        c.execute("INSERT INTO timestamps (type, timestamp) VALUES (?, ?)",
                  (action, readable_time))
        conn.commit()
        conn.close()
        return f"Recorded {action} at {readable_time}"
    return "No face detected"

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
