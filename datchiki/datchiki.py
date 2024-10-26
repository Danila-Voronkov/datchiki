import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

filter_last_minute = True  # Если True, показываем данные за последнюю минуту, иначе используем custom_period
custom_period = 5  # Период в минутах (может быть изменен пользователем)

#А тут был я АРтёмка
# Флаги для отслеживания состояния окон
is_humidity_window_open = False
is_temperature_window_open = False
is_light_window_open = False

# Функция для подключения к базе данных и получения данных
def fetch_data_from_db():
	conn = mysql.connector.connect(
		host="127.0.0.1",
		user="root",
		password="admin",
		database="datchiki"
	)
	
	cursor = conn.cursor()
	
	current_time = datetime.now()

	# Если фильтрация по последней минуте
	if filter_last_minute:
		time_threshold = current_time - timedelta(minutes=1)
		query = "SELECT * FROM sensor_data WHERE Time >= %s"
		cursor.execute(query, (time_threshold,))
	else:
		# Фильтр по custom_period (например, за последние N минут)
		time_threshold = current_time - timedelta(minutes=custom_period)
		query = "SELECT * FROM sensor_data WHERE Time >= %s"
		cursor.execute(query, (time_threshold,))

	result = cursor.fetchall()

	# Преобразуем данные в pandas DataFrame
	df = pd.DataFrame(result, columns=["sensor_data_id","value", "time", "sensor_id"])  # Укажите названия ваших столбцов
	cursor.close()
	conn.close()
	return df

# Функция для обновления графика
def update_graph(frame, ax, message_label):
	ax.cla()  # Очистка предыдущего графика

	# Получение данных из БД
	df = fetch_data_from_db()

	# Пример построения графика: ось X — время, ось Y — значение
	ax.plot(df['time'], df['value'], marker='o', color='black')
	ax.set_xlabel('Время')
	ax.set_ylabel('Влажность в %')
	ax.set_title('Показатель влажности почвы')
	ax.set_ylim(0, 100)  # Установить пределы по оси Y

	# Добавляем область ниже 20 и выше 80 с красноватым цветом
	ax.axhspan(0, 20, facecolor='red', alpha=0.1)
	ax.axhspan(80, 100, facecolor='red', alpha=0.1)

	# Добавляем текстовое сообщение в зависимости от значений
	if not df.empty:  # Проверяем, что DataFrame не пуст
		avg_value = df['value'].mean()  # Среднее значение

		if avg_value < 20:
			message = "Требуется полив"
		elif avg_value > 80:
			message = "Почва слишком влажная"
		else:
			message = "Влажность в норме"

		# Обновляем текстовое сообщение
		if avg_value < 20 or avg_value > 80:
			message_label.config(text=message, fg='darkred')
		else:
			message_label.config(text=message, fg='black')

# Функция для закрытия окна и сброса флага
def on_window_close(window, flag):
	global is_humidity_window_open, is_temperature_window_open, is_light_window_open
	window.destroy()  # Закрываем окно
	if flag == "humidity":
		is_humidity_window_open = False
	elif flag == "temperature":
		is_temperature_window_open = False
	elif flag == "light":
		is_light_window_open = False

# Функция для отображения графика в модальном окне
def show_plot():
	global is_humidity_window_open
	if is_humidity_window_open:
		return  # Если окно уже открыто, ничего не делаем
	is_humidity_window_open = True

	modal_window = Toplevel(root)
	modal_window.title("Влажность")
	modal_window.resizable(True, True)  # Разрешаем изменение размера окна
	modal_window.configure(bg="#f5f5f5")
	modal_window.minsize(600, 600)  # Минимальная ширина и высота
	modal_window.protocol("WM_DELETE_WINDOW", lambda: on_window_close(modal_window, "humidity"))  # Закрытие окна

	# Создаем фигуру и ось
	fig, ax = plt.subplots()

	# Создаем текстовое сообщение
	message_label = tk.Label(modal_window, text="", font=('Helvetica', 12))
	message_label.pack(pady=10)  # Добавляем отступ для лучшего отображения

	# Настройка анимации графика
	ani = animation.FuncAnimation(fig, lambda frame: update_graph(frame, ax, message_label), interval=1000)  # Обновление каждую секунду

	# Встраиваем график в модальное окно
	canvas = FigureCanvasTkAgg(fig, master=modal_window)
	canvas.draw()
	canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Разрешаем масштабирование графика

# Функция-заглушка для модального окна с температурой
def show_temperature():
	global is_temperature_window_open
	if is_temperature_window_open:
		return  # Если окно уже открыто, ничего не делаем
	is_temperature_window_open = True

	modal_window = Toplevel(root)
	modal_window.title("Температура")
	modal_window.resizable(True, True)
	modal_window.configure(bg="#f5f5f5")
	modal_window.minsize(600, 400)  # Минимальная ширина и высота
	modal_window.protocol("WM_DELETE_WINDOW", lambda: on_window_close(modal_window, "temperature"))  # Закрытие окна

	# Здесь будет реализована логика для отображения графика или данных температуры
	tk.Label(modal_window, text="График температуры. Логика будет добавлена позже.", font=('Helvetica', 12)).pack(pady=20)

# Функция-заглушка для модального окна с освещенностью
def show_light():
	global is_light_window_open
	if is_light_window_open:
		return  # Если окно уже открыто, ничего не делаем
	is_light_window_open = True

	
	modal_window = Toplevel(root)
	modal_window.title("Освещенность")
	modal_window.resizable(True, True)
	modal_window.configure(bg="#f5f5f5")
	modal_window.minsize(600, 400)  # Минимальная ширина и высота
	modal_window.protocol("WM_DELETE_WINDOW", lambda: on_window_close(modal_window, "light"))  # Закрытие окна

	# Здесь будет реализована логика для отображения графика или данных освещенности
	tk.Label(modal_window, text="График освещенности. Логика будет добавлена позже.", font=('Helvetica', 12)).pack(pady=20)

# Основное окно
root = tk.Tk()
root.title("Меню мониторинга")
root.geometry("600x400")  # Размер окна
root.configure(bg="#e0f7fa")  # Цвет фона
root.minsize(600, 400)  # Минимальная ширина и высота
root.maxsize(600, 400)  # Минимальная ширина и высота

# Заголовок
title_label = tk.Label(root, text="Система мониторинга", font=('Helvetica', 18, 'bold'), bg="#e0f7fa")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Левый фрейм для кнопок
left_frame = tk.Frame(root, bg="#e0f7fa")
left_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

# Правый фрейм для изображения
right_frame = tk.Frame(root, bg="#e0f7fa")
right_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

# Стили кнопок
button_style = {'font': ('Helvetica', 12), 'bg': '#4caf50', 'fg': 'white', 'activebackground': '#388e3c', 'activeforeground': 'white', 'width': 36}

# Кнопки с фиксированной шириной
plot_button = tk.Button(left_frame, text="Показать график влажности почвы", command=show_plot, **button_style)
plot_button.pack(pady=10, fill=tk.X)

temp_button = tk.Button(left_frame, text="Показать график температуры", command=show_temperature, **button_style)
temp_button.pack(pady=10, fill=tk.X)

light_button = tk.Button(left_frame, text="Показать график освещенности", command=show_light, **button_style)
light_button.pack(pady=10, fill=tk.X)

# Загрузка изображения горшка с цветком
image = Image.open("C:/Users/danil/Downloads/geran.png")  # Путь к изображению
image = image.resize((200, 200), Image.LANCZOS)  # Изменение размера изображения
flower_image = ImageTk.PhotoImage(image)

# Добавляем изображение в правый фрейм
image_label = tk.Label(right_frame, image=flower_image, bg="#e0f7fa")
image_label.pack(pady=10)

# Установка пропорционального масштабирования
root.grid_rowconfigure(0, weight=1)  # Заголовок
root.grid_rowconfigure(1, weight=1)  # Контент
root.grid_columnconfigure(0, weight=1)  # Левый фрейм
root.grid_columnconfigure(1, weight=1)  # Правый фрейм

root.mainloop()