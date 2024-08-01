from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Kết nối đến MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attendance_db"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read_rfid', methods=['POST'])
def read_rfid():
    data = request.get_json()
    card_uid = data['card_uid']
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO attendance (card_uid) VALUES (%s)", (card_uid,))
    db.commit()
    cursor.close()
    
    return jsonify({'status': 'success', 'card_uid': card_uid})

@app.route('/attendance_list', methods=['GET'])
def attendance_list():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attendance ORDER BY timestamp DESC")
    attendance_records = cursor.fetchall()
    cursor.close()
    return jsonify(attendance_records)

if __name__ == '__main__':
    app.run(debug=True)
