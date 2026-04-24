from flask import Flask, request, jsonify
import pymysql
import os
import re

app = Flask(__name__)

# -----------------------------
# DB CONNECTION
# -----------------------------
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

# -----------------------------
# INPUT VALIDATION (ANTI-INJECTION)
# -----------------------------
def is_valid_name(name):
    if not name or len(name.strip()) == 0:
        return False

    # block common SQL keywords / symbols
    blacklist = [
        "select", "insert", "delete", "drop",
        "update", "--", ";", "/*", "*/", "xp_"
    ]

    name_lower = name.lower()

    for word in blacklist:
        if word in name_lower:
            return False

    # allow only letters, numbers, spaces
    return re.match("^[a-zA-Z0-9 ]+$", name) is not None


# -----------------------------
# GET ITEMS (SEARCH + PAGINATION)
# -----------------------------
@app.route('/items', methods=['GET'])
def get_items():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 5))
        search = request.args.get('search', '')

        offset = (page - 1) * limit

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM item WHERE name LIKE %s LIMIT %s OFFSET %s",
            (f"%{search}%", limit, offset)
        )
        data = cursor.fetchall()

        cursor.execute(
            "SELECT COUNT(*) as total FROM item WHERE name LIKE %s",
            (f"%{search}%",)
        )
        total = cursor.fetchone()['total']

        conn.close()

        return jsonify({
            "data": data,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# CREATE (NO DUPLICATES)
# -----------------------------
@app.route('/items', methods=['POST'])
def create_item():
    try:
        data = request.json
        name = data.get('name', '').strip()

        # validation
        if not is_valid_name(name):
            return jsonify({"error": "Invalid input"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        # check duplicate
        cursor.execute("SELECT * FROM item WHERE name=%s", (name,))
        if cursor.fetchone():
            return jsonify({"error": "Duplicate entry not allowed"}), 400

        cursor.execute("INSERT INTO item (name) VALUES (%s)", (name,))
        conn.commit()
        conn.close()

        return jsonify({"message": "created"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# UPDATE (NO DUPLICATES)
# -----------------------------
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    try:
        data = request.json
        name = data.get('name', '').strip()

        if not is_valid_name(name):
            return jsonify({"error": "Invalid input"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        # check duplicate excluding current id
        cursor.execute(
            "SELECT * FROM item WHERE name=%s AND id!=%s",
            (name, id)
        )
        if cursor.fetchone():
            return jsonify({"error": "Duplicate entry not allowed"}), 400

        cursor.execute(
            "UPDATE item SET name=%s WHERE id=%s",
            (name, id)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "updated"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# DELETE
# -----------------------------
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM item WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
