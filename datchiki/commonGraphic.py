import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime, timedelta
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


timestamps = []  # Для хранения временных меток
sensor_data = {
    1: [],  # Данные для датчика 1
    2: [],  # Данные для датчика 2
}
visibility = {1: True, 2: True}  # Управление видимостью для каждого датчика
strikethrough = {1: False, 2: False}  # Управление зачеркиванием названий

# Список цветов для датчиков
colors = {
    1: 'black',
    2: 'orange'
}

def main(frame):
    global timestamps, sensor_data  # Указываем, что используем глобальные переменные

    # Инициализация данных
    timestamps = [datetime.now() - timedelta(seconds=i) for i in range(100)]
    sensor_data[1] = np.random.normal(25, 5, 100)  # Данные для датчика 1
    sensor_data[2] = np.random.normal(30, 5, 100)  # Данные для датчика 2

    # Создаем фигуру и ось для графика
    fig, ax = plt.subplots(figsize=(10, 6))

    # Функция для обновления данных на графике
    def update_graph(i):
        ax.clear()  # Очищаем ось перед перерисовкой

        # Обновляем временные метки и данные
        global timestamps
        timestamps = timestamps[1:] + [datetime.now()]
        sensor_data[1] = np.append(sensor_data[1][1:], np.random.normal(25, 5))
        sensor_data[2] = np.append(sensor_data[2][1:], np.random.normal(30, 5))


        # Отображаем данные каждого датчика, если он видим
        for sensor_id in [1, 2]:
            if visibility[sensor_id]:  # Проверяем видимость датчика
                ax.plot(timestamps, sensor_data[sensor_id], label=f"Sensor {sensor_id}", 
                        color=colors[sensor_id])
            else:
                # Линия не видима, но все равно добавляем ее для отображения в легенде
                ax.plot(timestamps, sensor_data[sensor_id], label=f"Sensor {sensor_id}", 
                        color=colors[sensor_id], alpha=0)  # Прозрачная линия

        # Создаем легенду в контейнере
        legend = ax.legend(loc="upper left", bbox_to_anchor=(1, 1), frameon=False)  # Размещаем легенду
        for legend_text in legend.get_texts():  # Устанавливаем для текста кликабельность
            legend_text.set_picker(True)

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

        # Обновляем цвет текста в легенде
        if visibility[sensor_id]:
            legend.set_color(colors[sensor_id])  # Возвращаем цвет, если видимо
        else:
            legend.set_color('red')  # Изменяем цвет на красный, если скрыто

        fig.canvas.draw()

    # Подключаем событие выбора на легенде
    fig.canvas.mpl_connect("pick_event", on_pick)

    # Настройка анимации для обновления графика
    ani = animation.FuncAnimation(fig, update_graph, interval=1000)


    # Добавление графика в окно Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill='both', expand=True)
    canvas.draw()