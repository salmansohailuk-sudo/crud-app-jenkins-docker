from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)




# Function to create DB connection
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),        # RDS endpoint
        user=os.getenv("DB_USER"),        # DB username
        password=os.getenv("DB_PASS"),    # DB password
        database=os.getenv("DB_NAME"),    # DB name
        cursorclass=pymysql.cursors.DictCursor
    )

# READ all items
@app.route('/items', methods=['GET'])
def get_items():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM item")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

# CREATE item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO item (name) VALUES (%s)", (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "created"})

# DELETE item
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM item WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted"})

# Start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
