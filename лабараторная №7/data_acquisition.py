import random

class DataAcquisition:
    def __init__(self):
        pass

    def get_sensor_data(self):
        temperature = round(random.uniform(15, 35), 1)
        humidity = round(random.uniform(30, 80), 1)
        light = round(random.uniform(100, 1000), 1)
        return {
            'temperature': temperature,
            'humidity': humidity,
            'light': light
        }