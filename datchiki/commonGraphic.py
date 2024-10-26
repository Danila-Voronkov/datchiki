import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
from datetime import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ����������� � ���� ������
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

# ������������� ���� Tkinter
root = tk.Tk()
root.title("������ ������ ��������")

# ������� ������ � ��� ��� �������
fig, ax = plt.subplots()

# ������� ��� �������� ����� � ��������� ���������
lines = {}
visibility = {1: True, 2: True}  # ���������� ���������� ��� ������� �������

# ������� ��� ���������� ������ �� �������
def update_graph(i):
    data = get_data_from_db()
    ax.clear()  # ������� ��� ����� ������������
    
    # ��������� ������ �� sensor_id
    for sensor_id in [1, 2]:
        sensor_data = data[data['sensor_id'] == sensor_id]
        if not sensor_data.empty and visibility[sensor_id]:  # ��������� ��������� �������
            ax.plot(sensor_data['timestamp'], sensor_data['value'], label=f"Sensor {sensor_id}")

    ax.legend()  # ��������� �������
    ax.set_xlabel("�����")
    ax.set_ylabel("��������")
    ax.set_title("������ � ��������")

# ���������� ������ �� �������
def on_pick(event):
    legend = event.artist
    label = legend.get_text()
    sensor_id = int(label.split()[-1])  # �������� ����� ������� �� ������ �������

    # ����������� ��������� �������
    visibility[sensor_id] = not visibility[sensor_id]
    
    # ��������� ���� ������ �������
    legend.set_alpha(1.0 if visibility[sensor_id] else 0.2)
    fig.canvas.draw()

# ���������� ������� ������ �� �������
fig.canvas.mpl_connect("pick_event", on_pick)

# ��������� �������� ��� ���������� �������
ani = animation.FuncAnimation(fig, update_graph, interval=1000)

# ���������� ������� � ���� Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
canvas.draw()

# ������ ����������
root.mainloop()

