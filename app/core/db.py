# app/core/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "uptime_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            latency REAL,
            timestamp REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_log(result: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO logs (url, status, latency, timestamp)
        VALUES (?, ?, ?, ?)
    """, (result['url'], result['status'], result['latency'], result['timestamp']))
    conn.commit()
    conn.close()

def get_logs(limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url, status, latency, timestamp FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    logs = []
    for row in rows:
        logs.append({
            "url": row[0],
            "status": row[1],
            "latency": row[2],
            "timestamp": row[3]
        })
    return logs[::-1]  # reverse for chronological order
