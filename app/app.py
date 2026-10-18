import os
import sys
from flask import Flask
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "mydatabase")
DB_USER = os.environ.get("DB_USER", "dbuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

@app.route("/")
def hello():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f"🚀 Hello from Flask! Connected to PostgreSQL successfully: <br><code>{db_version[0]}</code>"
    except Exception as e:
        return f"❌ Database connection failed: <br><pre>{str(e)}</pre>", 500


@app.route("/api")
def api_root():
    return {"message": "Welcome to the API!"}, 200

@app.route("/api/health")
def api_health():
    return "OK", 200

@app.route("/api/crash")
def crash():
    os._exit(1)

@app.route("/api/add")
def add_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        # Create a simple table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Insert a row
        cur.execute("INSERT INTO visits DEFAULT VALUES;")
        conn.commit()
        cur.close()
        conn.close()
        return "✅ Successfully inserted a record into PostgreSQL!", 200
    except Exception as e:
        return f"❌ Failed to insert data: <pre>{str(e)}</pre>", 500

@app.route("/api/data")
def get_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT id, created_at FROM visits ORDER BY id DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"total_visits": len(rows), "records": rows}, 200
    except Exception as e:
        return f"❌ Failed to query data: <pre>{str(e)}</pre>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
