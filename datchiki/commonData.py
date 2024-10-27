import tkinter as tk
import numpy as np

# Глобальные переменные
sensor_data = {
    1: [],  # Данные для датчика 1
    2: [],  # Данные для датчика 2
}
event_message = ""  # Для хранения сообщений о событиях

def main(frame):
    global sensor_data, event_message  # Указываем, что используем глобальные переменные

    # Инициализация данных
    sensor_data[1] = np.random.normal(25, 5, 100)  # Данные для датчика 1
    sensor_data[2] = np.random.normal(30, 5, 100)  # Данные для датчика 2

    # Создаем контейнер для текстовых выводов (слева)
    event_frame = tk.Frame(frame)
    event_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

    # Текстовый виджет для вывода сообщений о событиях
    event_text_widget = tk.Text(event_frame, height=10, bg='lightyellow', font=('Arial', 12))
    event_text_widget.pack(fill=tk.BOTH, expand=True)
    event_text_widget.config(state=tk.DISABLED)  # Запрещаем редактирование

    # Создаем контейнер для текущих значений (справа)
    current_value_frame = tk.Frame(frame)
    current_value_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    # Текстовый виджет для отображения текущих значений
    current_value_text = tk.Text(current_value_frame, height=10, bg='lightgreen', font=('Arial', 12))
    current_value_text.pack(fill=tk.BOTH, expand=True)
    current_value_text.config(state=tk.DISABLED)  # Запрещаем редактирование

    # Функция для обновления данных и текстовых виджетов
    def update_data():
        global event_message

        # Обновляем данные для датчиков
        sensor_data[1] = np.append(sensor_data[1][1:], np.random.normal(25, 5))
        sensor_data[2] = np.append(sensor_data[2][1:], np.random.normal(30, 5))

        # Обновление текстового виджета с текущими значениями
        current_value_text.config(state=tk.NORMAL)  # Разрешаем редактирование
        current_value_text.delete(1.0, tk.END)  # Очищаем текстовое поле
        current_value_text.insert(tk.END, f"Sensor 1: {sensor_data[1][-1]:.2f}\n")  # Последнее значение датчика 1
        current_value_text.insert(tk.END, f"Sensor 2: {sensor_data[2][-1]:.2f}\n")  # Последнее значение датчика 2
        current_value_text.config(state=tk.DISABLED)  # Запрещаем редактирование

        # Проверка условий для вывода сообщений
        if sensor_data[1][-1] > 35:
            event_message = "Sensor 1: Очень высокое значение!"
        elif sensor_data[2][-1] < 15:
            event_message = "Sensor 2: Очень низкое значение!"
        else:
            event_message = "Все значения в норме."

        # Обновление текстового виджета с сообщением о событиях
        event_text_widget.config(state=tk.NORMAL)  # Разрешаем редактирование
        event_text_widget.delete(1.0, tk.END)  # Очищаем текстовое поле
        event_text_widget.insert(tk.END, event_message)  # Вставляем новое значение
        event_text_widget.config(state=tk.DISABLED)  # Запрещаем редактирование

        # Запланировать следующий вызов через 1 секунду
        frame.after(1000, update_data)

    # Запуск обновления данных
    update_data()

# Пример запуска приложения
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Секция 2")
    main(root)
    root.mainloop()