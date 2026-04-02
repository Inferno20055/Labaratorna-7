from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import threading
import uvicorn
import secrets

import config
from data_acquisition import DataAcquisition
from filter_module import FilterModule
from logger_module import Logger
from analytics_module import Analytics

# Создаём глобальные объекты
daq = DataAcquisition()
filter_mod = FilterModule(config.TEMP_HIGH, config.TEMP_LOW, config.HUMIDITY_THRESHOLD)
logger = Logger(config.LOG_FILE)
analytics = None  # Инициализация после получения N

# Настройки для basic auth
USERNAME = "admin"
PASSWORD = "lab2025"
security = HTTPBasic()

app = FastAPI()

def check_credentials(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials

# Эндпоинт - получить последние данные
@app.get("/api/last")
def get_last(credentials: HTTPBasicCredentials = Depends(security)):
    check_credentials(credentials)
    data = daq.get_sensor_data()
    return data

# Эндпоинт - статистика
@app.get("/api/stats")
def get_stats(n: int = 5, credentials: HTTPBasicCredentials = Depends(security)):
    global analytics
    check_credentials(credentials)
    if not analytics:
        analytics = Analytics(n)
    averages = analytics.get_averages()
    return averages

# Эндпоинт - запуск сбора данных
@app.post("/api/collect")
def collect_data(credentials: HTTPBasicCredentials = Depends(security)):
    check_credentials(credentials)
    data = daq.get_sensor_data()
    warnings = filter_mod.filter(data)
    message = f"Collected data: T={data['temperature']}, H={data['humidity']}, Light={data['light']}"
    logger.log(message)
    return {"status": "measurement collected", "data": data}

@app.get("/api/log")
def get_log(credentials: HTTPBasicCredentials = Depends(security)):
    check_credentials(credentials)
    return {"log": ["Лог пример 1", "Лог пример 2"]}

@app.post("/api/threshold")
def set_thresholds(thresholds: dict, credentials: HTTPBasicCredentials = Depends(security)):
    check_credentials(credentials)
    filter_mod.TEMP_HIGH = thresholds.get("temp_high", filter_mod.TEMP_HIGH)
    filter_mod.TEMP_LOW = thresholds.get("temp_low", filter_mod.TEMP_LOW)
    filter_mod.HUMIDITY_THRESHOLD = thresholds.get("humidity_threshold", filter_mod.HUMIDITY_THRESHOLD)
    return {"status": "thresholds updated", "thresholds": thresholds}

def run_server():
    uvicorn.run("server:app", host="127.0.0.1", port=8080, log_level="info")

if __name__ == "__main__":
    # Запрашиваем N для аналитики у пользователя
    N = int(input("Введите число N для аналитики: "))
    analytics = Analytics(N)

    # Запускаем API-сервер в отдельном потоке
    threading.Thread(target=run_server, daemon=True).start()
    print("API сервер запущен по адресу http://127.0.0.1:8080")
