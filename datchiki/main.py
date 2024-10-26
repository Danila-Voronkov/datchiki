import tkinter as tk
from tkinter import messagebox
import importlib

class SensorDataGenerator:
    # Предполагается, что у вас есть этот класс, который генерирует данные
    def __init__(self):
        self.mode_settings = {
            "humidity": "normal",
            "temperature": "normal",
            "light": "normal",
        }

    def set_mode(self, mode, sensor_type):
        self.mode_settings[sensor_type] = mode

    def generate_data(self):
        # Здесь должна быть логика генерации данных
        # Например, возвращение случайных данных в зависимости от режима
        return {
            "humidity": 50,  # Например, статическое значение
            "temperature": 22,  # Например, статическое значение
            "light_level": 300,  # Например, статическое значение
        }

class SensorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
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
        text = f"Влажность: {data['humidity']}%, Температура: {data['temperature']}°C, Уровень освещенности: {data['light_level']} люкс"
        self.label.config(text=text)
        self.after(1000, self.update_data)  # Обновляем данные каждую секунду

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.geometry("1280x720")

        # Основной фрейм для отображения содержимого разделов
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

        # Кнопки для переключения между разделами
        btn_section1 = tk.Button(self.root, text="Раздел 1", command=lambda: self.load_section("commonGraphic"))
        btn_section1.pack(side="left", fill="x", expand=True)

        btn_section2 = tk.Button(self.root, text="Раздел 2", command=lambda: self.load_section("dataGeneration"))
        btn_section2.pack(side="left", fill="x", expand=True)

        btn_section3 = tk.Button(self.root, text="Раздел 3", command=self.show_sensor_frame)
        btn_section3.pack(side="left", fill="x", expand=True)

        # Загрузка первого раздела по умолчанию
        self.load_section("commonGraphic")

    def load_section(self, module_name):
        try:
            module = importlib.import_module(module_name)
            # Очистка содержимого основного фрейма
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            # Вызов функции main() из модуля для добавления нового содержимого
            module.main(self.content_frame)
        except ModuleNotFoundError:
            messagebox.showerror("Ошибка", f"Модуль '{module_name}' не найден.")
        except AttributeError:
            messagebox.showerror("Ошибка", f"Модуль '{module_name}' не содержит функцию main().")

    def show_sensor_frame(self):
        # Очистка содержимого основного фрейма
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # Показать фрейм с кнопками датчиков
        sensor_frame = SensorFrame(self.content_frame)
        sensor_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
