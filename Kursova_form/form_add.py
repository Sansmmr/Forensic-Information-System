import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyodbc
from tkinter import ttk

entries = {}
id_entries = {}

server = 'DESKTOP-4MGRCV0'
database = 'crimedatabase3'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;timeout=10'


cases = [
        ("Детектив", "Фото детектива"),
        ("Підозрюваний", "Фото підозрюваного"),
        ("Потерпілий", "Фото потерпілого"),
        ("Свідок", "Фото свідка"),
        ]

def create_add_form():
        def submit():
        
            def insert_into_citizen_table(name, photo):
                cursor.execute("INSERT INTO Citizen (name, photo) VALUES (?, ?)", (name, photo))

            def insert_into_detectives_table(citizen_id, position, rank, investigating_authorities_id):
                cursor.execute("""
                    INSERT INTO detective (id_citizen, position, rang, id_investigating_authorities)
                    VALUES (?, ?, ?, ?)
                    """, (citizen_id, position, rank, investigating_authorities_id))

            def insert_into_victim_table(citizen_id):
                cursor.execute("INSERT INTO victim (fk_citizen) VALUES (?)", (citizen_id))
            
            def insert_into_witness_table(citizen_id):
                cursor.execute("INSERT INTO witness (fk_citizen) VALUES (?)", (citizen_id))
            
            def insert_into_suspect_table(citizen_id):
                cursor.execute("INSERT INTO suspect (fk_citizen) VALUES (?)", (citizen_id))

            def read_photo_data(file_path):
                with open(file_path, 'rb') as file:
                    return file.read()

            def insert_into_vid_crime_table(crime_id, crime_name):
                cursor.execute("INSERT INTO vid_crime (id, name) VALUES (?, ?)", (crime_id, crime_name))
                

            def insert_into_evidence_table(evidence_id, name, FK_types_of_evidence):
                cursor.execute("INSERT INTO evidence (id, name, FK_Types_of_evidence) VALUES (?, ?, ?)", (evidence_id, name, FK_types_of_evidence))
                
            
            def insert_investigating_authority():
                name = investigating_authority_entry.get()
                cursor.execute("INSERT INTO Investigating_authorities (name) VALUES (?)", (name,))

            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            for case in cases:  
                name = entries[case[0]].get()
                photo_path = entries[case[1]].get()
                id_entry = id_entries[case[0]].get() if case[0] in ["Свідок", "Потерпілий", "Підозрюваний"] else None

                insert_into_citizen_table(name, read_photo_data(photo_path))
                conn.commit()

                cursor.execute("SELECT IDENT_CURRENT('Citizen')")
                citizen_id = cursor.fetchone()[0]

                if case[0] == "Свідок":
                    insert_into_witness_table(citizen_id)
                    insert_into_vid_crime_table(crime_id_entry.get(), crime_name_entry.get())
                    insert_into_evidence_table(evidence_id_entry.get(), evidence_name_entry.get(), evidence_type_entry.get())
                    insert_investigating_authority()

                elif case[0] == "Потерпілий":
                    insert_into_victim_table(citizen_id)

                elif case[0] == "Підозрюваний":
                    insert_into_suspect_table(citizen_id)

                elif case[0] == "Детектив":
                    insert_into_detectives_table(citizen_id, position_entry.get(), rank_entry.get(), investigating_authorities_id_entry.get())

                conn.commit()


            conn.close()
            messagebox.showinfo("info", "Данні успішно добавлено у систему")
        
        root = tk.Toplevel()
        root.title("Форма для введення даних")

        style = ttk.Style()
        style.configure('TEntry', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))

        for case in cases:
            label = ttk.Label(root, text=case[0])
            label.pack()
            entries[case[0]] = ttk.Entry(root)
            entries[case[0]].pack()

            if case[0] != "Детектив":
                id_label = ttk.Label(root, text=f"ID {case[0]}")
                id_label.pack()
                id_entries[case[0]] = ttk.Entry(root)
                id_entries[case[0]].pack()

            photo_label = ttk.Label(root, text=case[1])
            photo_label.pack()
            entries[case[1]] = ttk.Entry(root)
            entries[case[1]].pack()

        investigating_authority_label = ttk.Label(root, text="Ім'я слідчого органу:")
        investigating_authority_label.pack()
        investigating_authority_entry = ttk.Entry(root)
        investigating_authority_entry.pack()

        investigating_authorities_id_label = ttk.Label(root, text="ID слідчого органу")
        investigating_authorities_id_label.pack()
        investigating_authorities_id_entry = ttk.Entry(root)
        investigating_authorities_id_entry.pack()

        position_label = ttk.Label(root, text="Посада детектива")
        position_label.pack()
        position_entry = ttk.Entry(root)
        position_entry.pack()

        rank_label = ttk.Label(root, text="Ранг детектива")
        rank_label.pack()
        rank_entry = ttk.Entry(root)
        rank_entry.pack()

        # Fields for vid_crime
        crime_id_label = ttk.Label(root, text="ID виду злочину:")
        crime_id_label.pack()
        crime_id_entry = ttk.Entry(root)
        crime_id_entry.pack()

        crime_name_label = ttk.Label(root, text="Назва виду злочину:")
        crime_name_label.pack()
        crime_name_entry = ttk.Entry(root)
        crime_name_entry.pack()

        # Fields for evidence
        evidence_type_label = ttk.Label(root, text="Вид доказу (ID):")
        evidence_type_label.pack()
        evidence_type_entry = ttk.Entry(root)
        evidence_type_entry.pack()

        evidence_name_label = ttk.Label(root, text="Ім'я доказу:")
        evidence_name_label.pack()
        evidence_name_entry = ttk.Entry(root)
        evidence_name_entry.pack()

        evidence_id_label = ttk.Label(root, text="ID доказу:")
        evidence_id_label.pack()
        evidence_id_entry = ttk.Entry(root)
        evidence_id_entry.pack()

        submit_button = ttk.Button(root, text="Відправити", command=submit)
        submit_button.pack()

        result_label = ttk.Label(root, text="")
        result_label.pack()

        def select_photo(field_name):
            file_path = filedialog.askopenfilename()
            entries[field_name].delete(0, tk.END)
            entries[field_name].insert(0, file_path)

        for field_name in entries:
            if field_name.startswith("Фото"):
                browse_button = ttk.Button(root, text=f"Вибрати {field_name}", command=lambda field_name=field_name: select_photo(field_name))
                browse_button.pack()
            # create_next_form()