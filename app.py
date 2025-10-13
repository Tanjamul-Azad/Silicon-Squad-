from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

def get_latest_data():
    db = mysql.connector.connect(
        host="localhost",
        user="care_user",         # use the same user you created
        password="care_pass",     # same password
        database="care_companion"
    )
    cursor = db.cursor()
    cursor.execute("SELECT gas, flame, temperature, humidity, pulse, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    db.close()
    if row:
        return {
            "gas": row[0],
            "flame": row[1],
            "temperature": row[2],
            "humidity": row[3],
            "pulse": row[4],
            "timestamp": str(row[5])
        }
    return {}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    return jsonify(get_latest_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
