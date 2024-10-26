import tkinter as tk
from dataGeneration import SensorDataGenerator

class App:
    def __init__(self):
        self.generator = SensorDataGenerator()

        self.root = tk.Tk()
        self.root.title("Датчики")
        self.root.geometry("400x300")

        self.label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.label.pack()

        # Кнопки для управления режимами для влажности
        tk.Button(self.root, text="Влажность: Нормальный", command=lambda: self.set_mode("normal", "humidity")).pack()
        tk.Button(self.root, text="Влажность: Завышенный", command=lambda: self.set_mode("high", "humidity")).pack()
        tk.Button(self.root, text="Влажность: Заниженный", command=lambda: self.set_mode("low", "humidity")).pack()

        # Кнопки для управления режимами для температуры
        tk.Button(self.root, text="Температура: Нормальный", command=lambda: self.set_mode("normal", "temperature")).pack()
        tk.Button(self.root, text="Температура: Завышенный", command=lambda: self.set_mode("high", "temperature")).pack()
        tk.Button(self.root, text="Температура: Заниженный", command=lambda: self.set_mode("low", "temperature")).pack()

        # Кнопки для управления режимами для освещенности
        tk.Button(self.root, text="Освещенность: Нормальный", command =lambda: self.set_mode("normal", "light")).pack()
        tk.Button(self.root, text="Освещенность: Завышенный", command=lambda: self.set_mode("high", "light")).pack()
        tk.Button(self.root, text="Освещенность: Заниженный", command=lambda: self.set_mode("low", "light")).pack()

        self.update_data()

    def set_mode(self, mode, sensor_type):
        self.generator.set_mode(mode, sensor_type)

    def update_data(self):
        data = self.generator.generate_data()
        text = f"Влажность: {data['humidity']}%, Температура: {data['temperature']}°C, Уровень освещенности: {data['light_level']} люкс"
        self.label.config(text=text)
        self.root.after(1000, self.update_data)  # Обновляем данные каждую секунду

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()