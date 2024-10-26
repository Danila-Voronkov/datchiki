import tkinter as tk

def main():
    window = tk.Toplevel()
    window.title("Файл 1")
    window.geometry("300x200")
    label = tk.Label(window, text="Это окно для файла 1")
    label.pack(pady=20)
    window.mainloop()