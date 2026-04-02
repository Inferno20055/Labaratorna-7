import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, message):
        try:
            with open(self.filename, 'a') as f:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'[{timestamp}] {message}\n')
        except Exception as e:
            print(f"Ошибка при записи в лог: {e}")