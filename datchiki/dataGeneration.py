import random
import time
import mysql.connector
import tkinter as tk

class SensorDataGenerator:
    def __init__(self):
        # Начальные значения для датчиков
        self.humidity = 50.0  # Начальная влажность
        self.temperature = 22.0  # Начальная температура
        self.light_level = 500.0  # Начальный уровень освещенности
        self.humidity_mode = "normal"  
        self.temperature_mode = "normal"  
        self.light_mode = "normal"

        self.running = True  # Флаг для управления циклом генерации данных

    def set_mode(self, mode, sensor_type):
        """Устанавливает режим генерации данных для указанного датчика."""
        if sensor_type == "humidity":
            self.humidity_mode = mode
        elif sensor_type == "temperature":
            self.temperature_mode = mode
        elif sensor_type == "light":
            self.light_mode = mode

    def generate_humidity(self):
        mode = self.humidity_mode
        if mode == "normal":
            change = random.uniform(-1, 1)
        elif mode == "high":
            change = random.uniform(1, 3)
        elif mode == "low":
            change = random.uniform(-3, -1)
        
        self.humidity = max(0, min(100, self.humidity + change))
        return round(self.humidity, 2)

    def generate_temperature(self):
        mode = self.temperature_mode
        if mode == "normal":
            change = random.uniform(-0.5, 0.5)
        elif mode == "high":
            change = random.uniform(0.5, 1.5)
        elif mode == "low":
            change = random.uniform(-1.5, -0.5)
        
        self.temperature = max(-30, min(50, self.temperature + change))
        return round(self.temperature, 2)

    def generate_light_level(self):
        mode = self.light_mode
        if mode == "normal":
            change = random.uniform(-10, 10)
        elif mode == "high":
            change = random.uniform(10, 20)
        elif mode == "low":
            change = random.uniform(-20, -10)
        
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
            (data['temperature'], timestamp, 2),  # Температура
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
    
    def start_generating(self, update_callback):
        while self.running:
            data = self.generate_data()
            update_callback(data)
            time.sleep(1)  # Ждем 1 секунду перед генерацией новых данных

    def stop(self):
        self.running = False


class SensorFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.generator = SensorDataGenerator()

        self.label = tk.Label(self, text="", font=("Helvetica", 16))
        self.label.pack()

        # Кнопки для управления режимами для влажности
        tk.Button(self, text="Влажность: Нормальный", command=lambda: self.set_mode("normal", "humidity")).pack()
        tk.Button(self, text="Влажность: Завышенный", command=lambda: self.set_mode("high", "humidity")).pack()
        tk.Button(self, text="Влажность: Заниженный", command=lambda: self.set_mode("low", "humidity")).pack()

        # Кнопки для управления режимами для температуры
        tk.Button(self, text="Температура: Нормальный", command=lambda: self.set_mode("normal", "temperature")).pack()
        tk.Button(self, text="Температура: Завышенный", command=lambda: self.set_mode("high", "temperature")).pack()
        tk.Button(self, text="Температура: Заниженный", command=lambda: self.set_mode("low", "temperature")).pack()

        # Кнопки для управления режимами для освещенности
        tk.Button(self, text="Освещенность: Нормальный", command=lambda: self.set_mode("normal", "light")).pack()
        tk.Button(self, text="Освещенность: Завышенный", command=lambda: self.set_mode("high", "light")).pack()
        tk.Button(self, text="Освещенность: Заниженный", command=lambda: self.set_mode("low", "light")).pack()

        self.update_data()

    def set_mode(self, mode, sensor_type):
        self.generator.set_mode(mode, sensor_type)

    def update_data(self):
        data = self.generator.generate_data()
        self.generator.save_to_database(data)
        text = f"Влажность: {data['humidity']}%, Температура: {data['temperature']}°C, Уровень освещенности: {data['light_level']} люкс"
        self.label.config(text=text)
        self.after(1000, self.update_data)  # Обновляем данные каждую секунду

def main(parent_frame):
    """Функция для инициализации интерфейса в переданном фрейме."""
    frame = SensorFrame(parent_frame)
    frame.pack(fill="both", expand=True)
