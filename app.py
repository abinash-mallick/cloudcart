import os
from flask import Flask, jsonify, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "shopdb")
DB_USER = os.getenv("DB_USER", "shopuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "shoppass")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(120) NOT NULL,
            description TEXT,
            price NUMERIC(10,2) NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)
    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]

    if count == 0:
        products = [
            ("Wireless Headphones", "Bluetooth over-ear headphones", 2499.00, 25),
            ("Smart Watch", "Fitness and notification smartwatch", 3299.00, 18),
            ("Laptop Stand", "Adjustable aluminum laptop stand", 1499.00, 40),
            ("USB-C Hub", "6-in-1 USB-C hub", 1899.00, 30),
            ("Travel Backpack", "Water-resistant laptop backpack", 2199.00, 15)
        ]
        cur.executemany(
            "INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)",
            products
        )
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as exc:
        return jsonify({"status": "unhealthy", "error": str(exc)}), 503

@app.route("/api/products", methods=["GET"])
def products():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, description, price, stock FROM products ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json(silent=True) or {}

    required = ["name", "description", "price", "stock"]
    if any(field not in data for field in required):
        return jsonify({"error": "name, description, price and stock are required"}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        INSERT INTO products (name, description, price, stock)
        VALUES (%s, %s, %s, %s)
        RETURNING id, name, description, price, stock
        """,
        (data["name"], data["description"], data["price"], data["stock"])
    )
    product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(product), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
