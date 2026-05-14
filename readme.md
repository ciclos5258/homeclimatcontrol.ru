
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

---

👨‍💻 Author  
[github](https://github.com/ciclos5258)  
[mail](ciclos52582@gmail.com)  
[telegram](https://t.me/rendich76)