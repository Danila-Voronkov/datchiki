import tkinter as tk
from dataGeneration import SensorDataGenerator

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Генератор данных с датчиков")

        self.generator = SensorDataGenerator()

        self.label = tk.Label(master, text="Выберите режим генерации данных:")
        self.label.pack()

        self.normal_button = tk.Button(master, text="Нормальные данные", command=self.set_normal_mode)
        self.normal_button.pack()

        self.high_button = tk.Button(master, text="Завышенные данные", command=self.set_high_mode)
        self.high_button.pack()

        self.low_button = tk.Button(master, text="Заниженные данные", command=self.set_low_mode)
        self.low_button.pack()

        self.data_label = tk.Label(master, text="")
        self.data_label.pack()

        self.generate_data()

    def set_normal_mode(self):
        self.generator.set_mode("normal")
        self.data_label.config(text="Режим: Нормальные данные")

    def set_high_mode(self):
        self.generator.set_mode("high")
        self.data_label.config(text="Режим: Завышенные данные")

    def set_low_mode(self):
        self.generator.set_mode("low")
        self.data_label.config(text="Режим: Заниженные данные")

    def generate_data(self):
        # Генерация данных с датчиков
        data = self.generator.generate_data()

        # Обновление метки с данными
        self.data_label.config(
            text=f"Влажность: {data['humidity']}%, "
                 f" Температура: {data['temperature']}°C, "
                 f"Освещенность: {data['light_level']} люкс"
        )

        # Сохранение данных в базу данных
        self.generator.save_to_database(data)

        # Запланировать следующую генерацию данных через 1 секунду
        self.master.after(1000, self.generate_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()