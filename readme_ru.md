```markdown
# 🌡️ Climat Monitor — IoT-система мониторинга климата

Полноценная IoT-система для удалённого мониторинга температуры и влажности в реальном времени. Состоит из микроконтроллера ESP32 с датчиком DHT22, серверной части на Flask + MQTT и веб-интерфейса с графиками на Chart.js.

**Стек:**
- **Backend:** Python (Flask, paho-MQTT)
- **ESP32:** C++ (WiFi, PubSubClient, DHT sensor library)
- **Frontend:** JavaScript (native), HTML, CSS

---

## 📁 Структура проекта

```
homeclimatcontrol.ru/
├── backend/
│   ├── server.py
│   └── sensors.db
└── frontend/
    ├── index.html
    ├── style.css
    └── chart.js
```

## 🚀 Возможности

- 📡 Приём данных с ESP32 по MQTT-протоколу
- 💾 Сохранение измерений в SQLite
- 📊 REST API с эндпоинтами: все данные, последнее измерение, статистика
- 📈 Визуализация истории температуры и влажности (Chart.js)
- 🔒 HTTPS через Nginx + Let's Encrypt
- 🔄 Обновление данных через MQTT WebSocket (опционально)

---

## 🔧 Архитектура

```
ESP32 + DHT22
     │
     ▼ (MQTT, топик esp32/sensors)
┌──────────┐     ┌─────────┐
│ Mosquitto│────▶│Flask App│───▶ SQLite
│  Broker  │     │(порт5002)│
└──────────┘     └────┬─────┘
                      │ (REST API)
                      ▼
                 ┌──────────┐
                 │  Nginx   │
                 │(HTTPS:443)│
                 └────┬─────┘
                      ▼
               Веб-интерфейс
            (homeclimatcontrol.ru)
```

## 📡 API

| Метод | Эндпоинт      | Описание                         |
|-------|---------------|----------------------------------|
| GET   | `/api/data`   | Последние 1000 записей           |
| GET   | `/api/latest` | Последнее измерение              |
| GET   | `/api/stats`  | Статистика (avg, min, max)       |

## 📊 Веб-интерфейс

- Текущие показания температуры и влажности в реальном времени
- Интерактивный график истории (Chart.js)
- Адаптивный дизайн
- Отображение статуса подключения

## 🔐 Безопасность

- MQTT с аутентификацией по логину и паролю
- Flask работает на localhost (недоступен извне напрямую)
- Nginx выступает HTTPS-прокси с сертификатом Let's Encrypt
- CORS настроен только для разрешённых источников
```

👨‍💻 Автор
[github](https://github.com/ciclos5258)
[mail](ciclos52582@gmail.com)
[telegram](https://t.me/rendich76)