from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB = "cancer_data.db"


def init_db():
    conn = sqlite3.connect(DB)
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
            confidence TEXT,
            created_at TEXT
        );
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("cancer_detection.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        main_image = request.files.get("main_image")
        patch_image = request.files.get("patch_image")

        if main_image is None:
            return jsonify({"error": "Main image missing"}), 400

        model = request.form.get("model")
        detected_class = request.form.get("detected_class")
        subtype_code = request.form.get("subtype_code")
        subtype_name = request.form.get("subtype_name")
        confidence = request.form.get("confidence")

        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute("""
            INSERT INTO analysis (
                main_image, patch_image, main_filename, patch_filename,
                model_used, detected_class, subtype_code, subtype_name,
                confidence, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            main_image.read(),
            patch_image.read() if patch_image else None,
            main_image.filename,
            patch_image.filename if patch_image else None,
            model,
            detected_class,
            subtype_code,
            subtype_name,
            confidence
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/records", methods=["GET"])
def records():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT id, main_filename, patch_filename, detected_class,
               subtype_code, subtype_name, confidence, created_at
        FROM analysis
    """)
    rows = c.fetchall()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "main_filename": r[1],
            "patch_filename": r[2],
            "class": r[3],
            "subtype_code": r[4],
            "subtype_name": r[5],
            "confidence": r[6],
            "created_at": r[7]
        }
        for r in rows
    ])


if __name__ == "__main__":
    init_db()
    print("Backend running: http://127.0.0.1:5000")
    app.run(debug=True)
