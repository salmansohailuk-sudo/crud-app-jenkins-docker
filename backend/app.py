from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# DB connection
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

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
# CREATE
# -----------------------------
@app.route('/items', methods=['POST'])
def create_item():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO item (name) VALUES (%s)", (data['name'],))
        conn.commit()
        conn.close()
        return jsonify({"message": "created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# UPDATE
# -----------------------------
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE item SET name=%s WHERE id=%s", (data['name'], id))
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
# CHART STATS
# -----------------------------
# -----------------------------
# PIE CHART STATS (TOTAL RECORDS)
# -----------------------------
# -----------------------------
# PIE CHART (MEANINGFUL BREAKDOWN)
# -----------------------------
@app.route('/stats/chart', methods=['GET'])
def chart_stats():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Group data: A vs Others
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN LOWER(name) LIKE 'a%%' THEN 'Starts with A'
                    ELSE 'Others'
                END as label,
                COUNT(*) as count
            FROM item
            GROUP BY label
        """)

        rows = cursor.fetchall()
        conn.close()

        labels = [row['label'] for row in rows]
        values = [row['count'] for row in rows]

        return jsonify({
            "labels": labels,
            "values": values
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
