import json
import sqlite3
import threading
from datetime import datetime
import paho.mqtt.client as mqtt
from flask import Flask, jsonify
from flask_cors import CORS

DB_PATH = "sensors.db"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/sensors"

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sensors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temp REAL NOT NULL,
                hum REAL NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

def save_reading(timestamp, temp, hum):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO sensors (timestamp, temp, hum) VALUES (?, ?, ?)",
            (timestamp, temp, hum)
        )
        conn.commit()
    finally:
        conn.close()

# Исправленный колбэк on_connect – теперь 5 аргументов (версия 2 API)
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"MQTT connected with code {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        temp = float(payload["temperature"])
        hum = float(payload["humidity"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_reading(timestamp, temp, hum)
        print(f"Saved: {timestamp}, {temp}, {hum}")
    except Exception as e:
        print("MQTT message error:", e)

# Создаём клиент с правильной версией API
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set("python", "pythonpassword")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

@app.route('/api/data', methods=['GET'])
def get_all_data():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, temp, hum
            FROM sensors
            ORDER BY timestamp DESC
            LIMIT 1000
        """)
        rows = cursor.fetchall()
        rows.reverse()

        data = {
            "success": True,
            "data": [
                {
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "temperature": row["temp"],
                    "humidity": row["hum"]
                }
                for row in rows
            ],
            "count": len(rows)
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/latest', methods=['GET'])
def get_latest():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, temp, hum
            FROM sensors
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        row = cursor.fetchone()

        if row:
            return jsonify({
                "success": True,
                "data": {
                    "timestamp": row["timestamp"],
                    "temperature": row["temp"],
                    "humidity": row["hum"]
                }
            })
        return jsonify({"success": False, "error": "Нет данных"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total FROM sensors")
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT AVG(temp) AS avg_temp, AVG(hum) AS avg_hum FROM sensors")
        avg = cursor.fetchone()

        cursor.execute("""
            SELECT MIN(temp) AS min_temp, MAX(temp) AS max_temp,
                   MIN(hum) AS min_hum, MAX(hum) AS max_hum
            FROM sensors
        """)
        minmax = cursor.fetchone()

        return jsonify({
            "success": True,
            "data": {
                "total_readings": total,
                "avg_temperature": round(avg["avg_temp"], 1) if avg["avg_temp"] is not None else None,
                "avg_humidity": round(avg["avg_hum"], 1) if avg["avg_hum"] is not None else None,
                "min_temperature": minmax["min_temp"],
                "max_temperature": minmax["max_temp"],
                "min_humidity": minmax["min_hum"],
                "max_humidity": minmax["max_hum"]
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

def start_mqtt():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    init_db()
    #threading.Thread(target=start_mqtt, daemon=True).start()
    print("🚀 Flask API server running on port 5002")
    app.run(host='0.0.0.0', port=5002, debug=False)