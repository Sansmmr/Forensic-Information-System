import tkinter as tk
import io
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pyodbc
import datetime
from PIL import Image, ImageTk



server = 'DESKTOP-4MGRCV0'
database = 'crimedatabase3'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;timeout=10'

def create_input_form():
    global root    
    root = tk.Toplevel()
    root.title('перегляд даних')

# Розміщення кнопки за допомогою grid()
    citizen_button = tk.Button(root, text='Показати дані громадян', command=lambda: fetch_citizen_data(root))
    citizen_button.grid(row=0, column=0, padx=10, pady=10)

    detective_button = tk.Button(root, text='Показати дані детективів', command=lambda: fetch_detective_data(root))
    detective_button.grid(row=1, column=0, padx=10, pady=10)

    evidence_button = tk.Button(root, text='Показати типи доказів', command=fetch_evidence_types)
    evidence_button.grid(row=2, column=0, padx=10, pady=10)


    crime_button = tk.Button(root, text='Показати типи злочинів', command=fetch_crime_types)
    crime_button.grid(row=3, column=0, padx=10, pady=10)


    investigation_button = tk.Button(root, text='Показати дані розслідування', command=fetch_investigation_data)
    investigation_button.grid(row=4, column=0, padx=10, pady=10)


    authorities_button = tk.Button(root, text='Показати дані слідчих органів', command=fetch_authorities_data)
    authorities_button.grid(row=5, column=0, padx=10, pady=10)


    victim_button = tk.Button(root, text='Показати дані постраждалих', command=lambda: fetch_victim_data(root))
    victim_button.grid(row=6, column=0, padx=10, pady=10)


    witness_button = tk.Button(root, text='Показати дані свідків', command=lambda: fetch_witness_data(root))
    witness_button.grid(row=7, column=0, padx=10, pady=10)


    suspect_button = tk.Button(root, text='Показати дані підозрюваних', command=lambda: fetch_suspect_data(root))
    suspect_button.grid(row=8, column=0, padx=10, pady=10)



    crime_button = tk.Button(root, text='Показати дані про злочин', command=fetch_crime_data)
    crime_button.grid(row=9, column=0, padx=10, pady=10)

    detectives_in_button = tk.Button(root, text='Показати дані про взаємодію детективів у розслідуванні', command=fetch_detectives_in_data)
    detectives_in_button.grid(row=10, column=0, padx=10, pady=10)

    evidence_button = tk.Button(root, text='Показати дані доказів', command=fetch_evidence_data)
    evidence_button.grid(row=11, column=0, padx=10, pady=10)


    

    


def fetch_citizen_data(root):
    def show_citizens(rows, display_window):
        for idx, row in enumerate(rows):
            citizen_label = tk.Label(frame, text=f'ID: {row.id}, Name: {row.name}')
            citizen_label.grid(row=idx, column=0, padx=10, pady=5)

            if row.photo:
                image = Image.open(io.BytesIO(row.photo))
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                photo_label = tk.Label(frame, image=photo)
                photo_label.image = photo
                photo_label.grid(row=idx, column=1, padx=10, pady=5)

    def search_citizen():
        search_term = search_entry.get()
        for widget in frame.winfo_children():
            widget.destroy()

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            if search_term.isdigit():
                cursor.execute('SELECT id, name, photo FROM Citizen WHERE id = ?', (search_term,))
            else:
                cursor.execute('SELECT id, name, photo FROM Citizen WHERE name LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Громадянина не знайдено.")
            else:
                result_label.config(text="")
                show_citizens(rows, display_window)

            conn.close()
        except Exception as e:
            print(f"Error: {e}")

    display_window = tk.Toplevel(root)
    display_window.title('Дані громадян')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або ім'ям: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_citizen)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, photo FROM Citizen')
    rows = cursor.fetchall()

    show_citizens(rows, display_window)

    conn.close()

def fetch_detective_data(root):
    def show_detectives(rows, display_window):
        for idx, row in enumerate(rows):
            detective_label = tk.Label(frame, text=f'ID: {row.id}, Name: {row.citizen_name}, Position: {row.position}, Rank: {row.rang}')
            detective_label.grid(row=idx, column=0, padx=10, pady=5)

            try:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute('SELECT photo FROM citizen WHERE id = ?', (row.citizen_id,))
                photo_data = cursor.fetchone()

                if photo_data and photo_data[0]:
                    image = Image.open(io.BytesIO(photo_data[0]))
                    image = image.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    photo_label = tk.Label(frame, image=photo)
                    photo_label.image = photo
                    photo_label.grid(row=idx, column=1, padx=10, pady=5)
                    
                conn.close()
            except Exception as e:
                print(f"Error fetching photo: {e}")

    def search_detective():
        search_term = search_entry.get()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        try:
            for widget in frame.winfo_children():
                widget.destroy()

            cursor.execute('''
                SELECT d.id, c.id AS citizen_id, c.name AS citizen_name, d.position, d.rang 
                FROM detective d 
                JOIN citizen c ON d.id_citizen = c.id 
                WHERE LOWER(c.name) LIKE ? OR LOWER(d.position) LIKE ? OR LOWER(d.rang) LIKE ?''',
                           (f'%{search_term.lower()}%', f'%{search_term.lower()}%', f'%{search_term.lower()}%'))
            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Детектива не знайдено.")
            else:
                result_label.config(text="")
                show_detectives(rows, display_window)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.id, c.id AS citizen_id, c.name AS citizen_name, d.position, d.rang 
        FROM detective d 
        JOIN citizen c ON d.id_citizen = c.id''')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані детективів')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ім'ям детектива, посадою або рангом: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_detective)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    show_detectives(rows, display_window)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()




def fetch_evidence_types():
    def search_evidence():
        search_term = search_entry.get()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Очищення рамки перед виведенням нових результатів
        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.isdigit():
                cursor.execute('SELECT id, evidence_type FROM Types_of_evidence WHERE id = ?', (search_term,))
            else:
                cursor.execute('SELECT id, evidence_type FROM Types_of_evidence WHERE evidence_type LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Доказу не знайдено.")
            else:
                result_label.config(text="")
                for idx, row in enumerate(rows):
                    evidence_label = tk.Label(frame, text=f'ID: {row.id}, Evidence Type: {row.evidence_type}')
                    evidence_label.grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT id, evidence_type FROM Types_of_evidence')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Типи доказів')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або типом доказу: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_evidence)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        evidence_label = tk.Label(frame, text=f'ID: {row.id}, Evidence Type: {row.evidence_type}')
        evidence_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()

def fetch_crime_types():
    def search_crime():
        search_term = search_entry.get()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Очищення рамки перед виведенням нових результатів
        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.isdigit():
                cursor.execute('SELECT id, name FROM vid_crime WHERE id = ?', (search_term,))
            else:
                cursor.execute('SELECT id, name FROM vid_crime WHERE name LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Типу злочину не знайдено.")
            else:
                result_label.config(text="")
                for idx, row in enumerate(rows):
                    crime_label = tk.Label(frame, text=f'ID: {row.id}, Crime Type: {row.name}')
                    crime_label.grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM vid_crime')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Типи злочинів')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або типом злочину: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_crime)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        crime_label = tk.Label(frame, text=f'ID: {row.id}, Crime Type: {row.name}')
        crime_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()



def fetch_investigation_data():
    def search_investigation():
        search_term = search_entry.get().lower()  # Перетворення введеного терміну до нижнього регістру
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Очищення рамки перед виведенням нових результатів
        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.isdigit():
                cursor.execute('SELECT id, description, start_date, end_date, status FROM investigation WHERE id = ?', (search_term,))
            else:
                # Перевірка, чи введений термін - дата
                try:
                    # Перевірка формату дати
                    datetime.datetime.strptime(search_term, '%Y-%m-%d')
                    cursor.execute('SELECT id, description, start_date, end_date, status FROM investigation WHERE start_date = ? OR end_date = ?', (search_term, search_term))
                except ValueError:
                    # Пошук за регістронезалежним description та status
                    cursor.execute('SELECT id, description, start_date, end_date, status FROM investigation WHERE LOWER(description) LIKE ? OR LOWER(status) LIKE ?', (f'%{search_term}%', f'%{search_term}%'))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Розслідування не знайдено.")
            else:
                result_label.config(text="")
                for idx, row in enumerate(rows):
                    investigation_label = tk.Label(frame, text=f'ID: {row.id}, Description: {row.description}, Start Date: {row.start_date}, End Date: {row.end_date}, Status: {row.status}')
                    investigation_label.grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT id, description, start_date, end_date, status FROM investigation')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані розслідування')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID, датою чи статусом: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_investigation)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        investigation_label = tk.Label(frame, text=f'ID: {row.id}, Description: {row.description}, Start Date: {row.start_date}, End Date: {row.end_date}, Status: {row.status}')
        investigation_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()


def fetch_authorities_data():
    def search_authorities():
        search_term = search_entry.get().lower()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.isdigit():
                cursor.execute('SELECT id, name FROM Investigating_authorities WHERE id = ?', (search_term,))
            else:
                cursor.execute('SELECT id, name FROM Investigating_authorities WHERE LOWER(name) LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Слідчі органи не знайдено.")
            else:
                result_label.config(text="")
                for idx, row in enumerate(rows):
                    authorities_label = tk.Label(frame, text=f'ID: {row.id}, Name: {row.name}')
                    authorities_label.grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM Investigating_authorities')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані слідчих органів')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або назвою органу: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_authorities)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        authorities_label = tk.Label(frame, text=f'ID: {row.id}, Name: {row.name}')
        authorities_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()

def fetch_victim_data(root):
    def show_victims(rows, display_window):
        for idx, row in enumerate(rows):
            victim_label = tk.Label(frame, text=f'ID: {row.victim_id}, Citizen Name: {row.citizen_name}')
            victim_label.grid(row=idx, column=0, padx=10, pady=5)

            try:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute('SELECT photo FROM citizen WHERE id = ?', (row.citizen_id,))
                photo_data = cursor.fetchone()

                if photo_data and photo_data[0]:
                    image = Image.open(io.BytesIO(photo_data[0]))
                    image = image.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    photo_label = tk.Label(frame, image=photo)
                    photo_label.image = photo
                    photo_label.grid(row=idx, column=1, padx=10, pady=5)
                    
                conn.close()
            except Exception as e:
                print(f"Error fetching photo: {e}")

    def search_victim():
        search_term = search_entry.get().lower()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.startswith('c') and search_term[1:].isdigit():
                cursor.execute('SELECT v.id AS victim_id, c.id AS citizen_id, c.name AS citizen_name FROM victim v JOIN citizen c ON v.fk_citizen = c.id WHERE c.name LIKE ?', (f'%{search_term[1:]}%',))
            elif search_term.isdigit():
                cursor.execute('SELECT v.id AS victim_id, c.id AS citizen_id, c.name AS citizen_name FROM victim v JOIN citizen c ON v.fk_citizen = c.id WHERE v.id = ?', (search_term,))
            else:
                cursor.execute('SELECT v.id AS victim_id, c.id AS citizen_id, c.name AS citizen_name FROM victim v JOIN citizen c ON v.fk_citizen = c.id WHERE LOWER(c.name) LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Постраждалі не знайдено.")
            else:
                result_label.config(text="")
                show_victims(rows, display_window)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT v.id AS victim_id, v.fk_citizen AS citizen_id, c.name AS citizen_name FROM victim v JOIN citizen c ON v.fk_citizen = c.id')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані постраждалих')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або ім'ям громадянина: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_victim)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    show_victims(rows, display_window)

    for idx, row in enumerate(rows):
        victim_label = tk.Label(frame, text=f'ID: {row.victim_id}, Citizen Name: {row.citizen_name}')
        victim_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()



def fetch_witness_data(root):
    def show_witnesses(rows, display_window):
        for idx, row in enumerate(rows):
            witness_label = tk.Label(frame, text=f'ID: {row.witness_id}, Citizen Name: {row.citizen_name}')
            witness_label.grid(row=idx, column=0, padx=10, pady=5)

            if row.photo:
                image = Image.open(io.BytesIO(row.photo))
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                photo_label = tk.Label(frame, image=photo)
                photo_label.image = photo
                photo_label.grid(row=idx, column=1, padx=10, pady=5)

    def search_witness():
        search_term = search_entry.get().lower()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.startswith('c') and search_term[1:].isdigit():
                cursor.execute('SELECT w.id AS witness_id, c.name AS citizen_name, c.photo FROM witness w JOIN citizen c ON w.fk_citizen = c.id WHERE c.name LIKE ?', (f'%{search_term[1:]}%',))
            elif search_term.isdigit():
                cursor.execute('SELECT w.id AS witness_id, c.name AS citizen_name, c.photo FROM witness w JOIN citizen c ON w.fk_citizen = c.id WHERE w.id = ?', (search_term,))
            else:
                cursor.execute('SELECT w.id AS witness_id, c.name AS citizen_name, c.photo FROM witness w JOIN citizen c ON w.fk_citizen = c.id WHERE LOWER(c.name) LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Свідки не знайдені.")
            else:
                result_label.config(text="")
                show_witnesses(rows, display_window)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT w.id AS witness_id, c.name AS citizen_name, c.photo FROM witness w JOIN citizen c ON w.fk_citizen = c.id')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані свідків')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або ім'ям громадянина: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_witness)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        witness_label = tk.Label(frame, text=f'ID: {row.witness_id}, Citizen Name: {row.citizen_name}')
        witness_label.grid(row=idx, column=0, padx=10, pady=5)

        if row.photo:
            image = Image.open(io.BytesIO(row.photo))
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            photo_label = tk.Label(frame, image=photo)
            photo_label.image = photo
            photo_label.grid(row=idx, column=1, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()

    
def fetch_suspect_data(root):
    def show_suspects(rows, display_window):
        for idx, row in enumerate(rows):
            suspect_label = tk.Label(frame, text=f'ID: {row.id}, Citizen Name: {row.name}')
            suspect_label.grid(row=idx, column=0, padx=10, pady=5)

            # Додавання відображення фотографії
            if row.photo:
                image = Image.open(io.BytesIO(row.photo))
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                photo_label = tk.Label(frame, image=photo)
                photo_label.image = photo
                photo_label.grid(row=idx, column=1, padx=10, pady=5)

    def search_suspect():
        search_term = search_entry.get().lower()
        for widget in frame.winfo_children():
            widget.destroy()

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Запити SQL для пошуку підозрюваних за ID, номером громадянина або іменем
            if search_term.startswith('c') and search_term[1:].isdigit():
                cursor.execute('SELECT s.id, c.name, c.photo FROM suspect s JOIN citizen c ON s.fk_citizen = c.id WHERE c.id = ?', (search_term[1:],))
            elif search_term.isdigit():
                cursor.execute('SELECT s.id, c.name, c.photo FROM suspect s JOIN citizen c ON s.fk_citizen = c.id WHERE s.id = ?', (search_term,))
            else:
                cursor.execute('SELECT s.id, c.name, c.photo FROM suspect s JOIN citizen c ON s.fk_citizen = c.id WHERE LOWER(c.name) LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Підозрювані не знайдені.")
            else:
                result_label.config(text="")
                show_suspects(rows, display_window)

            conn.close()
        except Exception as e:
            print(f"Error: {e}")

    display_window = tk.Toplevel(root)
    display_window.title('Дані підозрюваних')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або номером громадянина: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_suspect)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT s.id, c.name, c.photo FROM suspect s JOIN citizen c ON s.fk_citizen = c.id')
    rows = cursor.fetchall()

    # Виклик функції show_suspects для відображення підозрюваних
    show_suspects(rows, display_window)

    conn.close()





def fetch_evidence_data():
    def search_evidence():
        search_term = search_entry.get().lower()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.isdigit():
                cursor.execute('SELECT e.id, e.name, t.evidence_type FROM evidence e JOIN Types_of_evidence t ON e.FK_Types_of_evidence = t.id WHERE e.id = ?', (search_term,))
            else:
                cursor.execute('SELECT e.id, e.name, t.evidence_type FROM evidence e JOIN Types_of_evidence t ON e.FK_Types_of_evidence = t.id WHERE LOWER(e.name) LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Докази не знайдено.")
            else:
                result_label.config(text="")
                for idx, row in enumerate(rows):
                    evidence_label = tk.Label(frame, text=f'ID: {row.id}, Name: {row.name}, Evidence Type: {row.evidence_type}')
                    evidence_label.grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT e.id, e.name, t.evidence_type FROM evidence e JOIN Types_of_evidence t ON e.FK_Types_of_evidence = t.id')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані доказів')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID або назвою доказу: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_evidence)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        evidence_label = tk.Label(frame, text=f'ID: {row.id}, Name: {row.name}, Evidence Type: {row.evidence_type}')
        evidence_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()

def fetch_detectives_in_data():
    def search_detectives_in():
        search_term = search_entry.get().lower()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        for widget in frame.winfo_children():
            widget.destroy()

        try:
            if search_term.startswith('i') and search_term[1:].isdigit():
                cursor.execute('SELECT id_detective, id_investigation FROM detectives_in WHERE id_investigation = ?', (search_term[1:],))
            elif search_term.isdigit():
                cursor.execute('SELECT id_detective, id_investigation FROM detectives_in WHERE id_detective = ?', (search_term,))
            else:
                cursor.execute('SELECT id_detective, id_investigation FROM detectives_in WHERE LOWER(id_investigation) LIKE ?', (f'%{search_term}%',))

            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Дані про взаємодію детективів у розслідуванні не знайдено.")
            else:
                result_label.config(text="")
                for idx, row in enumerate(rows):
                    detectives_in_label = tk.Label(frame, text=f'Detective ID: {row.id_detective}, Investigation ID: {row.id_investigation}')
                    detectives_in_label.grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT id_detective, id_investigation FROM detectives_in')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані про взаємодію детективів у розслідуванні')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за ID детектива або ID розслідування: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_detectives_in)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        detectives_in_label = tk.Label(frame, text=f'Detective ID: {row.id_detective}, Investigation ID: {row.id_investigation}')
        detectives_in_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()

def fetch_crime_data():
    def search_crime():
        search_term = search_entry.get().lower()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        for widget in frame.winfo_children():
            widget.destroy()

        try:
            cursor.execute('SELECT address, id_vid_crime, id_detective, id_investigating_authorities, id_suspect, id_witness, id_victim, id_evidence, date, title FROM crime WHERE LOWER(address) LIKE ?', (f'%{search_term}%',))
            rows = cursor.fetchall()

            if not rows:
                result_label.config(text="Злочини за вказаною адресою не знайдено.")
            else:
                result_label.config(text="")
                for idx, row in enumerate(rows):
                    crime_label = tk.Label(frame, text=f'Address: {row.address}, Crime ID: {row.id_vid_crime}, Detective ID: {row.id_detective}, Authorities ID: {row.id_investigating_authorities}, Suspect ID: {row.id_suspect}, Witness ID: {row.id_witness}, Victim ID: {row.id_victim}, Evidence ID: {row.id_evidence}, Date: {row.date}, Title: {row.title}')
                    crime_label.grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            print(f"Error: {e}")

        conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT address, id_vid_crime, id_detective, id_investigating_authorities, id_suspect, id_witness, id_victim, id_evidence, date, title FROM crime')
    rows = cursor.fetchall()

    display_window = tk.Toplevel(root)
    display_window.title('Дані про злочин')

    search_frame = tk.Frame(display_window)
    search_frame.pack()

    search_label = tk.Label(search_frame, text="Пошук за адресою: ")
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text="Знайти", command=search_crime)
    search_button.grid(row=0, column=2)

    result_label = tk.Label(display_window, text="")
    result_label.pack()

    canvas = tk.Canvas(display_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(display_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows):
        crime_label = tk.Label(frame, text=f'Address: {row.address}, Crime ID: {row.id_vid_crime}, Detective ID: {row.id_detective}, Authorities ID: {row.id_investigating_authorities}, Suspect ID: {row.id_suspect}, Witness ID: {row.id_witness}, Victim ID: {row.id_victim}, Evidence ID: {row.id_evidence}, Date: {row.date}, Title: {row.title}')
        crime_label.grid(row=idx, column=0, padx=10, pady=5)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    conn.close()

