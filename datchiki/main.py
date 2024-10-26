import tkinter as tk
from tkinter import messagebox
import importlib

# Функция для загрузки модуля по названию
def load_module(module_name):
    try:
        module = importlib.import_module(module_name)
        module.main()  # предполагаем, что в каждом модуле есть функция main()
    except ModuleNotFoundError:
        messagebox.showerror("Ошибка", f"Модуль '{module_name}' не найден.")
    except AttributeError:
        messagebox.showerror("Ошибка", f"Модуль '{module_name}' не содержит функцию main().")

# Функция для создания главного окна
def create_main_window():
    root = tk.Tk()
    root.title("Главное меню")
    root.geometry("400x300")

    # Создание меню
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    
    # Разделы меню и вызов файлов
    file_menu.add_command(label="Открыть файл 1", command=lambda: load_module("file1"))
    file_menu.add_command(label="Открыть файл 2", command=lambda: load_module("file2"))
    file_menu.add_command(label="Открыть файл 3", command=lambda: load_module("file3"))

    menu_bar.add_cascade(label="Файлы", menu=file_menu)

    # Добавление меню в окно
    root.config(menu=menu_bar)
    root.mainloop()

# Запуск основного окна
if __name__ == "__main__":
    create_main_window()