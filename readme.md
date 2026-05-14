[ru Читать на русском](readme_ru.md)

```markdown
# 🌡️ Climat Monitor — IoT Climate Monitoring System

A complete IoT system for remote, real-time temperature and humidity monitoring. It consists of an ESP32 microcontroller with a DHT22 sensor, a Flask + MQTT backend, and a web interface with Chart.js graphs.

**Stack:**
- **Backend:** Python (Flask, paho-MQTT)
- **ESP32:** C++ (WiFi, PubSubClient, DHT sensor library)
- **Frontend:** JavaScript (native), HTML, CSS

---

## 📁 Project Structure

homeclimatcontrol.ru/
├── backend/
│   ├── server.py
│   └── sensors.db
└── frontend/
    ├── index.html
    ├── style.css
    └── chart.js

## 🚀 Features

- 📡 Receive data from ESP32 via MQTT protocol
- 💾 Store measurements in SQLite
- 📊 REST API with endpoints: all data, latest measurement, statistics
- 📈 Visualization of temperature and humidity history (Chart.js)
- 🔒 HTTPS via Nginx + Let's Encrypt
- 🔄 Real-time data updates via MQTT WebSocket (optional)

---


## 🔧 Architecture


ESP32 + DHT22
     │
     ▼ (MQTT, topic esp32/sensors)
┌──────────┐     ┌─────────┐
│ Mosquitto│────▶│Flask App│───▶ SQLite
│  Broker  │     │(port5002)│
└──────────┘     └────┬─────┘
                      │ (REST API)
                      ▼
                 ┌──────────┐
                 │  Nginx   │
                 │(HTTPS:443)│
                 └────┬─────┘
                      ▼
               Web Interface
            (homeclimatcontrol.ru)


## 📡 API

| Method | Endpoint      | Description                         |
|--------|---------------|-------------------------------------|
| GET    | `/api/data`   | Latest 1000 records                 |
| GET    | `/api/latest` | Most recent measurement             |
| GET    | `/api/stats`  | Statistics (avg, min, max)          |

## 📊 Web Interface

- Real-time current temperature and humidity readings
- Interactive history chart (Chart.js)
- Responsive design
- Connection status display

## 🔐 Security

- MQTT with username/password authentication
- Flask runs on localhost (not directly exposed to the internet)
- Nginx acts as an HTTPS proxy with a Let's Encrypt certificate
- CORS configured for allowed origins only

👨‍💻 Author
[github](https://github.com/ciclos5258)
[mail](ciclos52582@gmail.com)
[telegram](https://t.me/rendich76)

```