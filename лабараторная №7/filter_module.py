class FilterModule:
    def __init__(self, temp_high, temp_low, humidity_threshold):
        self.temp_high = temp_high
        self.temp_low = temp_low
        self.humidity_threshold = humidity_threshold

    def filter(self, data):
        warnings = []
        alarm = False
        # Проверка температуры
        if data['temperature'] > self.temp_high:
            warnings.append('высокая температура')
        elif data['temperature'] < self.temp_low:
            warnings.append('низкая температура')
        # Проверка влажности
        if data['humidity'] > self.humidity_threshold:
            warnings.append('повышенная влажность')
        return warnings