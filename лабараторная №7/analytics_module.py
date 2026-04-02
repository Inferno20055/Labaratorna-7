class Analytics:
    def __init__(self, N):
        self.N = N
        self.data_history = {
            'temperature': [],
            'humidity': [],
            'light': []
        }

    def add_measurement(self, data):
        for key in self.data_history:
            self.data_history[key].append(data[key])
            if len(self.data_history[key]) > self.N:
                self.data_history[key].pop(0)

    def get_averages(self):
        averages = {}
        for key, values in self.data_history.items():
            if values:
                averages[key] = sum(values) / len(values)
            else:
                averages[key] = None
        return averages