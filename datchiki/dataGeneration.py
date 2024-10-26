import random
import time
import mysql.connector

class SensorDataGenerator:
    def __init__(self):
        # Начальные значения для датчиков
        self.humidity = 50.0  # Начальная влажность
        self.temperature = 22.0  # Начальная температура
        self.light_level = 500.0  # Начальный уровень освещенности
        self.mode = "normal"  # Режим по умолчанию

    def set_mode(self, mode):
        """Устанавливает режим генерации данных."""
        self.mode = mode

    def generate_humidity(self):
        if self.mode == "normal":
            change = random.uniform(-1, 1)
        elif self.mode == "high":
            change = random.uniform(1, 3)  # Увеличение для завышенного режима
        elif self.mode == "low":
            change = random.uniform(-3, -1)  # Уменьшение для заниженного режима
        
        self.humidity = max(0, min(100, self.humidity + change))
        return round(self.humidity, 2)

    def generate_temperature(self):
        if self.mode == "normal":
            change = random.uniform(-0.5, 0.5)
        elif self.mode == "high":
            change = random.uniform(0.5, 1.5)  # Увеличение для завышенного режима
        elif self.mode == "low":
            change = random.uniform(-1.5, -0.5)  # Уменьшение для заниженного режима
        
        self.temperature = max(-30, min(50, self.temperature + change))
        return round(self.temperature, 2)

    def generate_light_level(self):
        if self.mode == "normal":
            change = random.uniform(-10, 10)
        elif self.mode == "high":
            change = random.uniform(10, 20)  # Увеличение для завышенного режима
        elif self.mode == "low":
            change = random.uniform(-20, -10)  # Уменьшение для заниженного режима
        
        self.light_level = max(0, self.light_level + change)
        return round(self.light_level, 2)

    def save_to_database(self, data):
        """Сохраняет данные в базу данных MySQL"""
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin',
            database='datchiki'
        )
        
        cursor = connection.cursor()
        sql = "INSERT INTO sensor_data (value, time, sensor_id) VALUES (%s, %s, %s)"
        
        # Форматируем время
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['timestamp']))

        # Подготовка данных для вставки
        values = [
            (data['humidity'], timestamp, 1),  # Влажность
            (data['temperature'], timestamp, 2),     # Температура
            (data['light_level'], timestamp, 3)  # Освещенность
        ]
        
        cursor.executemany(sql, values)  # Выполняем вставку нескольких строк
        connection.commit()
        cursor.close()
        connection.close()

    def generate_data(self):
        # Генерация данных для всех датчиков
        humidity = self.generate_humidity()
        temperature = self.generate_temperature()
        light_level = self.generate_light_level()
        timestamp = time.time()  # Время в формате Unix

        return {
            'timestamp': timestamp,
            'humidity': humidity,
            'temperature': temperature,
            'light_level': light_level
        }