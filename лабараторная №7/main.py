from data_acquisition import DataAcquisition
from filter_module import FilterModule
from logger_module import Logger
from analytics_module import Analytics
import time
import sys
import os

# Импорт конфигурации
import config

def main():
    # Инициализация модулей
    daq = DataAcquisition()
    filter_mod = FilterModule(config.TEMP_HIGH, config.TEMP_LOW, config.HUMIDITY_THRESHOLD)
    logger = Logger(config.LOG_FILE)
    N = int(input("Введите число N для аналитики: "))
    analytics = Analytics(N)

    # Цикл из 10 итераций
    for i in range(1, 11):
        data = daq.get_sensor_data()
        warnings = filter_mod.filter(data)

        # Формируем сообщение
        if data['temperature'] > config.TEMP_HIGH:
            status = 'ALARM: высокая температура'
        elif data['temperature'] < config.TEMP_LOW:
            status = 'ALARM: низкая температура'
        elif data['humidity'] > config.HUMIDITY_THRESHOLD:
            status = 'Полив (повышенная влажность)'
        else:
            status = 'OK'

        # Логирование
        message = f"Т= {data['temperature']}°C, В= {data['humidity']}%, Освещенность= {data['light']} лк -> {status}"
        logger.log(message)

        # Вывод на экран
        print(f"[Замер {i}] {message}")


        analytics.add_measurement(data)
        if i % 3 == 0:
            averages = analytics.get_averages()
            print(f"\nАналитика за {N} замеров: средняя T={averages['temperature']:.1f}°C, "
                  f"средняя H={averages['humidity']:.1f}%, "
                  f"средний свет={averages['light']:.1f} лк\n")
        time.sleep(1)

if __name__ == "__main__":
    main()