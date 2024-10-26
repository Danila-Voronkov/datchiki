import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
from datetime import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Подключение к базе данных
def get_data_from_db():
    connection = mysql.connector.connect(
		host="127.0.0.1",
		user="root",
		password="admin",
		database="datchiki"
	)
    query = "SELECT sensor_id, timestamp, value FROM sensor_data ORDER BY timestamp DESC LIMIT 100"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Инициализация окна Tkinter
root = tk.Tk()
root.title("График данных датчиков")

# Создаем фигуру и ось для графика
fig, ax = plt.subplots()

# Словарь для хранения линий и состояния видимости
lines = {}
visibility = {1: True, 2: True}  # Управление видимостью для каждого датчика

# Функция для обновления данных на графике
def update_graph(i):
    data = get_data_from_db()
    ax.clear()  # Очищаем ось перед перерисовкой
    
    # Разделяем данные по sensor_id
    for sensor_id in [1, 2]:
        sensor_data = data[data['sensor_id'] == sensor_id]
        if not sensor_data.empty and visibility[sensor_id]:  # Проверяем видимость датчика
            ax.plot(sensor_data['timestamp'], sensor_data['value'], label=f"Sensor {sensor_id}")

    ax.legend()  # Добавляем легенду
    ax.set_xlabel("Время")
    ax.set_ylabel("Значение")
    ax.set_title("Данные с датчиков")

# Обработчик кликов на легенде
def on_pick(event):
    legend = event.artist
    label = legend.get_text()
    sensor_id = int(label.split()[-1])  # Получаем номер датчика из текста легенды

    # Переключаем видимость датчика
    visibility[sensor_id] = not visibility[sensor_id]
    
    # Обновляем цвет текста легенды
    legend.set_alpha(1.0 if visibility[sensor_id] else 0.2)
    fig.canvas.draw()

# Подключаем событие выбора на легенде
fig.canvas.mpl_connect("pick_event", on_pick)

# Настройка анимации для обновления графика
ani = animation.FuncAnimation(fig, update_graph, interval=1000)

# Добавление графика в окно Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
canvas.draw()

# Запуск приложения
root.mainloop()

