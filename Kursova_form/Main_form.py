import sys
import tkinter as tk
from tkinter import filedialog
import form_review
import form_add
import form_add_crime
import form_delete_crime


def exit_application():
    sys.exit()

def create_main_form():
    root = tk.Tk()
    root.title("Головне вікно")
    root.geometry("500x500")  # Змінити розмір вікна

    bg_color = "#f0f0f0"  # Колір фону

    label_style = {
        "font": ('Arial', 12),
        "bg": bg_color,
        "pady": 5
    }

    button_style = {
        "width": 40,
        "height": 4,
        "font": ('Arial', 13),
        "bg": "#4CAF50",  # Колір кнопки
        "fg": "white",    # Колір тексту на кнопці
        "activebackground": "#45a049",  # Колір при натисканні на кнопку
        "activeforeground": "white"
    }

    root.config(bg=bg_color)  # Встановлюємо колір фону для головного вікна

    label = tk.Label(root, text="Оберіть опцію:", **label_style)
    label.pack(pady=10)

    button1 = tk.Button(root, text="Додавання даних у систему", command=form_add.create_add_form, **button_style)
    button1.pack()

    button2 = tk.Button(root, text="Додавання даних у злочин", command=form_add_crime.create_crime_form, **button_style)
    button2.pack()

    button3 = tk.Button(root, text="Видалення даних у злочин", command=form_delete_crime.create_empty_form, **button_style)
    button3.pack()

    button4 = tk.Button(root, text="Перегляд даних", command=form_review.create_input_form, **button_style)
    button4.pack()

    button_exit = tk.Button(root, text="Вихід", command=exit_application, **button_style)
    button_exit.pack()

    root.mainloop()

create_main_form()
