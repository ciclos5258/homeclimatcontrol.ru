async function loadDataAndDrawChart() {
    try {
        // 1. Запрашиваем данные с сервера
        const response = await fetch('/api/data');
        if (!response.ok) {
            throw new Error('Ошибка загрузки данных');
        }

        const json = await response.json();
        if (!json.success) {
            throw new Error(json.error || 'Сервер вернул ошибку');
        }

        const records = json.data;

        // 2. Готовим массивы для графика
        const labels = records.map(record => record.timestamp);
        const temperatures = records.map(record => record.temperature);
        const humidities = records.map(record => record.humidity);

        const ctx = document.getElementById('tempChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Температура (°C)',
                        data: temperatures,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1,
                        pointRadius: 3
                    }
                ]
            },
            options: {
                responsive: true,
                animation: false,       // сразу показываем всю историю без прорисовки по точкам
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });

        // 3. Рисуем график (id canvas должен быть 'tempChart' – как в твоём HTML)
        const ctx2 = document.getElementById('tempChartTwo').getContext('2d');
        new Chart(ctx2, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Влажность (%)',
                        data: humidities,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        tension: 0.1,
                        pointRadius: 3
                    }
                ]
            },
            options: {
                responsive: true,
                animation: false,       // сразу показываем всю историю без прорисовки по точкам
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });

        

        

        // 4. Заполняем карточки последними актуальными значениями
        if (records.length > 0) {
            const last = records[records.length - 1];
            document.getElementById('temp').textContent = last.temperature;
            document.getElementById('hum').textContent = last.humidity;
            document.getElementById('temp-time').textContent = `⏱️ ${last.timestamp}`;
            document.getElementById('hum-time').textContent = `⏱️ ${last.timestamp}`;
            document.getElementById('device').innerHTML = '📱 Device: ESP32';
            document.getElementById('status').innerHTML = '✅ Данные загружены из базы';
            document.getElementById('raw').innerHTML = `Последняя запись: ${last.timestamp}`;
        } else {
            document.getElementById('raw').innerHTML = '⏳ Нет данных в базе';
        }
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('raw').innerHTML = `❌ Ошибка: ${error.message}`;
    }
}

window.addEventListener('load', loadDataAndDrawChart);