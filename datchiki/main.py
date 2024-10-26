import tkinter as tk
from tkinter import messagebox
import importlib

# Функция для загрузки раздела из модуля
def load_section(module_name):
    try:
        module = importlib.import_module(module_name)
        # Очистка содержимого основного фрейма
        for widget in content_frame.winfo_children():
            widget.destroy()
        # Вызов функции main() из модуля для добавления нового содержимого
        module.main(content_frame)
    except ModuleNotFoundError:
        messagebox.showerror("Ошибка", f"Модуль '{module_name}' не найден.")
    except AttributeError:
        messagebox.showerror("Ошибка", f"Модуль '{module_name}' не содержит функцию main().")

# Создаем главное окно
root = tk.Tk()
root.title("Главное меню")
root.geometry("1280x720")

# Основной фрейм для отображения содержимого разделов
content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True)

# Кнопки для переключения между разделами
btn_section1 = tk.Button(root, text="Раздел 1", command=lambda: load_section("commonGraphic"))
btn_section1.pack(side="left", fill="x", expand=True)

btn_section2 = tk.Button(root, text="Раздел 2", command=lambda: load_section("dataGeneration"))
btn_section2.pack(side="left", fill="x", expand=True)

btn_section3 = tk.Button(root, text="Раздел 3", command=lambda: load_section("section3"))
btn_section3.pack(side="left", fill="x", expand=True)

# Загрузка первого раздела по умолчанию
load_section("commonGraphic")

root.mainloop()