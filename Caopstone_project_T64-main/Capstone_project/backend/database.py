import sqlite3
import os

DB_NAME = "cancer_data.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_image BLOB,
                patch_image BLOB,
                main_filename TEXT,
                patch_filename TEXT,
                model_used TEXT,
                detected_class TEXT,
                subtype_code TEXT,
                subtype_name TEXT,
                confidence REAL,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()
        print(f"✓ Database initialized at: {os.path.abspath(DB_NAME)}")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        raise

if __name__ == "__main__":
    init_db()
