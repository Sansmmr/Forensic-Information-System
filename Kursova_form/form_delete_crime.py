import tkinter as tk
from tkinter import messagebox
import pyodbc

server = 'DESKTOP-4MGRCV0'
database = 'crimedatabase3'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'


def create_empty_form():
    empty_form = tk.Toplevel()
    empty_form.title("Форма для видалення даних про злочин")

    # Опис стилів
    entry_style = {
        "bg": "lightgray",
        "font": ('Arial', 12)
    }

    label_style = {
        "bg": "lightblue",
        "font": ('Arial', 12),
        "padx": 5,
        "pady": 5
    }

    # Створення елементів зі стилів
    crime_address_label = tk.Label(empty_form, text="Адреса:", **label_style)
    crime_address_label.pack()
    crime_address_entry = tk.Entry(empty_form, **entry_style)
    crime_address_entry.pack()

    crime_id__label = tk.Label(empty_form, text="ID виду злочину:", **label_style)
    crime_id__label.pack()
    crime_id__entry = tk.Entry(empty_form, **entry_style)
    crime_id__entry.pack()

    detective_id__label = tk.Label(empty_form, text="ID детектива:", **label_style)
    detective_id__label.pack()
    detective_id__entry = tk.Entry(empty_form, **entry_style)
    detective_id__entry.pack()

    investigating_authorities_id__label = tk.Label(empty_form, text="ID слідчого органу:", **label_style)
    investigating_authorities_id__label.pack()
    investigating_authorities_id__entry = tk.Entry(empty_form, **entry_style)
    investigating_authorities_id__entry.pack()

    suspect_id__label = tk.Label(empty_form, text="ID підозрюваного:", **label_style)
    suspect_id__label.pack()
    suspect_id__entry = tk.Entry(empty_form, **entry_style)
    suspect_id__entry.pack()

    witness_id__label = tk.Label(empty_form, text="ID свідка:", **label_style)
    witness_id__label.pack()
    witness_id__entry = tk.Entry(empty_form, **entry_style)
    witness_id__entry.pack()

    victim_id__label = tk.Label(empty_form, text="ID потерпілого:", **label_style)
    victim_id__label.pack()
    victim_id__entry = tk.Entry(empty_form, **entry_style)
    victim_id__entry.pack()

    evidence_id__label = tk.Label(empty_form, text="ID доказу:", **label_style)
    evidence_id__label.pack()
    evidence_id__entry = tk.Entry(empty_form, **entry_style)
    evidence_id__entry.pack()

    crime_date_label = tk.Label(empty_form, text="Дата:", **label_style)
    crime_date_label.pack()
    crime_date_entry = tk.Entry(empty_form, **entry_style)
    crime_date_entry.pack()

    crime_title_label = tk.Label(empty_form, text="Назва:", **label_style)
    crime_title_label.pack()
    crime_title_entry = tk.Entry(empty_form, **entry_style)
    crime_title_entry.pack()

    delete_button = tk.Button(empty_form, text="Видалити дані", command=lambda: delete_data(
        crime_address_entry, crime_id__entry, detective_id__entry,
        investigating_authorities_id__entry, suspect_id__entry,
        witness_id__entry, victim_id__entry, evidence_id__entry,
        crime_date_entry, crime_title_entry, conn_str)
    )
    delete_button.pack()


def delete_data(crime_address_entry, crime_id__entry, detective_id__entry,
                investigating_authorities_id__entry, suspect_id__entry,
                witness_id__entry, victim_id__entry, evidence_id__entry,
                crime_date_entry, crime_title_entry, conn_str):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    crime_address = crime_address_entry.get()
    crime_id = crime_id__entry.get()
    detective_id = detective_id__entry.get()
    investigating_authorities_id = investigating_authorities_id__entry.get()
    suspect_id = suspect_id__entry.get()
    witness_id = witness_id__entry.get()
    victim_id = victim_id__entry.get()
    evidence_id = evidence_id__entry.get()
    crime_date = crime_date_entry.get()
    crime_title = crime_title_entry.get()

    try:
        cursor.execute("DELETE FROM crime WHERE address = ? AND id_vid_crime = ? AND id_detective = ? AND "
                       "id_investigating_authorities = ? AND id_suspect = ? AND id_witness = ? AND id_victim = ? "
                       "AND id_evidence = ? AND date = ? AND title = ?",
                       (crime_address, crime_id, detective_id, investigating_authorities_id,
                        suspect_id, witness_id, victim_id, evidence_id, crime_date, crime_title))
        messagebox.showinfo("info", "Дані успішно видалено")
    except:
        messagebox.showinfo("info", "Помилка видалення")

    conn.commit()
    conn.close()
