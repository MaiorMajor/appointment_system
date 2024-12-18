import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from classes.user import User
from constants import *



class Menu:
    def __init__(self, root, admin=False):
        self.root = root
        self.admin = admin
        self.num_btns = 0
        self.root.title("Menu")
        self.root.geometry("1000x400")

        # Layout - main frame
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        self.show_dashboard()

    def show_dashboard(self):
        self.create_table()
        self.create_buttons()
    
    def create_buttons(self):
        """Creates the set of buttons at the bottom."""
        # Frame for buttons
        btn_lbl_frm = ttk.Frame(self.root)
        btn_lbl_frm.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Configure the frame to center the buttons
        btn_lbl_frm.columnconfigure(0, weight=1)

        # Sub-frame for buttons (inside the main frame)
        button_frame = ttk.Frame(btn_lbl_frm)
        button_frame.grid(row=0, column=0)

        # List of buttons and their respective commands
        buttons = [
            ("Add Consultation", self.add_consultation),
            ("Edit", self.edit_consultation),
            ("Delete", self.delete_consultations),
            ("Add Patient", self.add_patient),
        ]
        if self.admin:
            from gui.menu_admin import AdminMenu
            buttons.append(("Admin", lambda: AdminMenu(self.root)))

        # Add buttons to sub-frame and center them..
        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=10, pady=5)


    def create_table(self):
        """Creates the consultation table."""
        # Frame for the table
        table_frame = ttk.Frame(self.root)
        table_frame.grid(row=0, column=0, sticky="nsew")

        # Configure the frame to expand
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Create the treeview and configure columns
        self.table = ttk.Treeview(table_frame, columns=CONSULTATIONS_COLUMNS, show="headings")
        for col in CONSULTATIONS_COLUMNS:
            self.table.heading(col, text=col)


        # Scrollbars for the table
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        self.table.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Table and scrollbars layout
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
    
        self.load_appointments()

    def load_appointments(self):
        try:
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                # This query fetches all consultations sorted by date and time
                query = """
                    SELECT c.id, d.name, s.name, p.name, c.date || ' ' || c.time
                    FROM consultations c
                    JOIN doctor d ON c.doctor = d.id
                    JOIN specialization s ON d.specialization_id = s.id
                    JOIN patient p ON c.patient = p.id
                """
                #print("Executing query:", query)
                cursor.execute(query)
                rows = cursor.fetchall()
                from datetime import datetime,date
                
                # Get today's date
                today = date.today()

                # Filter out past consultations
                filtered_rows = [
                    row for row in rows
                    if datetime.strptime(row[-1], "%Y-%m-%d %H:%M").date() >= today
                ]

                # Sort filtered rows by date and time
                filtered_rows.sort(key=lambda row: datetime.strptime(row[-1], "%Y-%m-%d %H:%M"))
                #print(f"Number of rows fetched: {len(rows)}")

                # Clear existing items
                for item in self.table.get_children():
                    self.table.delete(item)
                    
                # Insert new data
                for row in filtered_rows:
                    #print(f"Inserting row: {row}")
                    self.table.insert('', 'end', values=row)
                    
        except sqlite3.Error as e:
            print("Database error:", e)


    def edit_consultation(self):
        """
        Opens a new window to edit the selected consultation details.
    
        This function retrieves the selected consultation from the table,
        extracts its details, and opens a new window where the user can
        modify the doctor, patient, date, and time associated with the
        consultation. The current values are pre-filled in the respective
        fields for easy editing.
        """
        selected_items = self.table.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a consultation to edit")
            return
            
        selected_item = selected_items[0]
        consultation_data = self.table.item(selected_item)['values']
        consultation_id = consultation_data[0]
        
        edit_window = tk.Toplevel()
        edit_window.title("Edit Consultation")
        edit_window.geometry("400x400")

        # Patient selection frame
        patient_frame = ttk.LabelFrame(edit_window, text="Select Patient")
        patient_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        patient_search = ttk.Entry(patient_frame)
        patient_search.insert(0, consultation_data[3])  # Set default value to current patient name
        patient_search.grid(row=0, column=0, padx=5, pady=5)

        patient_listbox = tk.Listbox(patient_frame, height=3)
        patient_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        add_patient_btn = ttk.Button(patient_frame, text="Add Patient", command=self.add_patient)
        add_patient_btn.grid(row=2, column=0, columnspan=2, pady=0)

        # Doctor selection frame
        # Doctor selection frame
        doctor_frame = ttk.LabelFrame(edit_window, text="Select Doctor")
        doctor_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        doctor_search = ttk.Entry(doctor_frame)
        doctor_search.insert(0, consultation_data[1])  # Set default value to current doctor name
        doctor_search.grid(row=0, column=0, padx=5, pady=5)

        doctor_listbox = tk.Listbox(doctor_frame, height=3)
        doctor_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Date and time entries
        ttk.Label(edit_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        date_entry = ttk.Entry(edit_window)
        date_entry.insert(0, consultation_data[4].split()[0])
        date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Time (HH:MM):").grid(row=3, column=0, padx=5, pady=5)
        time_entry = ttk.Entry(edit_window)
        time_entry.insert(0, consultation_data[4].split()[1])
        time_entry.grid(row=3, column=1, padx=5, pady=5)

        def format_date(event):
            text = date_entry.get().replace('-','')
            if len(text) > 8:
                date_entry.delete(8, tk.END)
                text = text[:8]
            if len(text) == 8:
                formatted = f"{text[:4]}-{text[4:6]}-{text[6:]}"
                date_entry.delete(0, tk.END)
                date_entry.insert(0, formatted)
                return 'break'

        def format_time(event):
            text = time_entry.get().replace(':','')
            if len(text) > 4:
                time_entry.delete(4, tk.END)
                text = text[:4]
            if len(text) == 4:
                formatted = f"{text[:2]}:{text[2:]}"
                time_entry.delete(0, tk.END)
                time_entry.insert(0, formatted)
                return 'break'

        date_entry.bind('<KeyRelease>', format_date)
        time_entry.bind('<KeyRelease>', format_time)

        def update_doctor_list(*args):
            search_term = doctor_search.get().lower()
            doctor_listbox.delete(0, tk.END)
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM doctor WHERE LOWER(name) LIKE ?", (f'%{search_term}%',))
                doctors = cursor.fetchall()
                for doctor in doctors:
                    doctor_listbox.insert(tk.END, doctor[0])

        def update_patient_list(*args):
            search_term = patient_search.get().lower()
            patient_listbox.delete(0, tk.END)
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM patient WHERE LOWER(name) LIKE ?", (f'%{search_term}%',))
                patients = cursor.fetchall()
                for patient in patients:
                    patient_listbox.insert(tk.END, patient[0])

        doctor_search.bind('<KeyRelease>', update_doctor_list)
        patient_search.bind('<KeyRelease>', update_patient_list)

        def on_doctor_select(event):
            if doctor_listbox.curselection():
                selection = doctor_listbox.get(doctor_listbox.curselection())
                doctor_search.delete(0, tk.END)
                doctor_search.insert(0, selection)

        def on_patient_select(event):
            if patient_listbox.curselection():
                selection = patient_listbox.get(patient_listbox.curselection())
                patient_search.delete(0, tk.END)
                patient_search.insert(0, selection)

        doctor_listbox.bind('<<ListboxSelect>>', on_doctor_select)
        patient_listbox.bind('<<ListboxSelect>>', on_patient_select)

        # Initial population of lists
        update_doctor_list()
        update_patient_list()

        def save_changes():
            try:
                import sqlite3
                from constants import PATH_TO_DB
                with sqlite3.connect(PATH_TO_DB) as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT id FROM doctor WHERE name = ?", (doctor_search.get(),))
                    doctor_id = cursor.fetchone()[0]
                    
                    cursor.execute(f"SELECT id FROM patient WHERE name = ?", (patient_search.get(),))
                    patient_id = cursor.fetchone()[0]
                    
                    cursor.execute("""
                        UPDATE consultations 
                        SET doctor = ?, patient = ?, date = ?, time = ?
                        WHERE id = ?
                    """, (
                        doctor_id,
                        patient_id,
                        date_entry.get(),
                        time_entry.get(),
                        consultation_id
                    ))
                    conn.commit()
                messagebox.showinfo("Success", "Consultation updated successfully")
                edit_window.destroy()
                self.load_appointments()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to update consultation: {str(e)}")

        ttk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_consultations(self):
        selected_items = self.table.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select one or more consultations to delete")
            return
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected consultations?")

        if confirmation:
            import sqlite3
            from constants import PATH_TO_DB
            from utils import consultation_exists_by_id

            for selected_item in selected_items:
                # Get the values from selected row
                consultation_data = self.table.item(selected_item)['values']
                consultation_id = consultation_data[0]
                print(f"Consultation exists before deleting: {consultation_exists_by_id(consultation_id)}")
                with sqlite3.connect(PATH_TO_DB) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM consultations WHERE id = ?", (consultation_id,))
                
                print(f"Consultation exists after deleting: {consultation_exists_by_id(consultation_id)}")

            messagebox.showinfo("Success", "Selected consultations deleted successfully")
            self.load_appointments()

    def add_consultation(self):
        add_window = tk.Toplevel()
        add_window.title("Add New Consultation")
        add_window.geometry("360x500")
    
        # Patient selection frame
        patient_frame = ttk.LabelFrame(add_window, text="Select Patient")
        patient_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    
        patient_search = ttk.Entry(patient_frame)
        patient_search.grid(row=0, column=0, padx=5, pady=5)
    
        patient_listbox = tk.Listbox(patient_frame, height=3)
        patient_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        add_patient_btn = ttk.Button(patient_frame, text="Add Patient", command=self.add_patient)
        add_patient_btn.grid(row=2, column=0, columnspan=2, pady=0)

        # Doctor selection frame
        doctor_frame = ttk.LabelFrame(add_window, text="Select Doctor")
        doctor_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    
        doctor_search = ttk.Entry(doctor_frame)
        doctor_search.grid(row=0, column=0, padx=5, pady=5)
    
        doctor_listbox = tk.Listbox(doctor_frame, height=3)
        doctor_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    
        # Date and time entries
        ttk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        date_entry = ttk.Entry(add_window)
        date_entry.grid(row=2, column=1, padx=5, pady=5)
    
        ttk.Label(add_window, text="Time (HH:MM):").grid(row=3, column=0, padx=5, pady=5)
        time_entry = ttk.Entry(add_window)
        time_entry.grid(row=3, column=1, padx=5, pady=5)

        from utils import format_date, format_time
        # Bind the formatting functions to the entries
        date_entry.bind('<KeyRelease>', lambda e: format_date(e, date_entry))
        time_entry.bind('<KeyRelease>', lambda e: format_time(e, time_entry))
        
        def update_patient_list(*args):
            search_term = patient_search.get().lower()
            patient_listbox.delete(0, tk.END)
            # Query database for patients matching search_term
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, email FROM patient WHERE LOWER(name) LIKE ?", (f'%{search_term}%',))
                for patient in cursor.fetchall():
                    patient_listbox.insert(tk.END, f"{patient[0]} ({patient[1]})")

        def update_doctor_list(*args):
            search_term = doctor_search.get().lower()
            doctor_listbox.delete(0, tk.END)
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM doctor WHERE LOWER(name) LIKE ?", (f'%{search_term}%',))
                doctors = cursor.fetchall()
                for doctor in doctors:
                    doctor_listbox.insert(tk.END, doctor[0])

        # Bind search entries to update functions
        patient_search.bind('<KeyRelease>', update_patient_list)
        doctor_search.bind('<KeyRelease>', update_doctor_list)

        def on_patient_select(event):
            if patient_listbox.curselection():  # Check if there is a selection
                selection = patient_listbox.get(patient_listbox.curselection())
                patient_search.delete(0, tk.END)
                patient_search.insert(0, selection)

        def on_doctor_select(event):
            if doctor_listbox.curselection():  # Check if there is a selection
                selection = doctor_listbox.get(doctor_listbox.curselection())
                doctor_search.delete(0, tk.END)
                doctor_search.insert(0, selection)
                # Store the selection
                doctor_search.selection = selection

        # Bind the listbox selections to the handler functions
        patient_listbox.bind('<<ListboxSelect>>', on_patient_select)
        doctor_listbox.bind('<<ListboxSelect>>', on_doctor_select)
        
    
        # Initial population of lists
        update_patient_list()
        update_doctor_list()

        def save_consultation():
            # Get selections from search entries
            selected_patient = patient_search.get()
            selected_doctor = doctor_search.get()
            date = date_entry.get()
            time = time_entry.get()
            
            if not all([selected_patient, selected_doctor, date, time]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            # Extract email from patient string (format is "name (email)")
            patient_email = selected_patient.split('(')[1].rstrip(')')   
            
            # Example of what selected_patient and patient_email would look like:
            # selected_patient = "John Smith (john.smith@email.com)"
            # patient_email = "john.smith@email.com"
                     
            from utils import get_id
            # Get IDs from database
            patient = get_id(patient_email, "email", "patient")
            doctor = get_id(selected_doctor, "name", "doctor") #should be email
            
            # Add to database
            import sqlite3
            from constants import PATH_TO_DB
            
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO consultations (patient, doctor, date, time)
                    VALUES (?, ?, ?, ?)
                """, (patient, doctor, date, time))
            
            messagebox.showinfo("Success", "Consultation added successfully!")
            from utils import consultation_exists
            print(f"Consultation exists? {consultation_exists(patient, doctor)}")
            add_window.destroy()
            self.load_appointments()            
        
        # Add the save button at the bottom of the window
        save_btn = ttk.Button(add_window, text="Save Consultation", command=save_consultation)
        save_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Bind Enter key to save_consultation
        add_window.bind('<Return>', lambda e: save_consultation())
    
    def add_patient(self):
        # Create a new window to add a patient
        add_patient_window = tk.Toplevel()
        add_patient_window.title("Add Patient")
        add_patient_window.geometry("400x300")
        add_patient_window.resizable(True, True)

        def add_patient_to_db():
            """
            Adds a new patient to the database after validating input fields.
            
            This function:
            1. Retrieves values from entry fields
            2. Validates that all fields are filled
            3. Creates a new Patient object
            4. Checks if patient already exists in database
            5. If patient exists, prompts user to override existing data
            6. Adds or updates patient in database accordingly
            
            Returns:
                None
            
            Raises:
                messagebox.showerror: If any required field is empty
            """
            name = name_entry.get()
            address = address_entry.get()
            birth_date = birth_date_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            # Check if all fields are filled
            if not (name and address and birth_date and phone and email):
                messagebox.showerror("Error", "All fields must be filled.")
                return
            
            from classes.patient import Patient
            patient = Patient(name, address, birth_date, phone, email)
            if patient.exists_in_db():
                response = messagebox.askyesno("Patient Exists", "Patient already exists in the database. Do you want to override it with new data?")                
                if response:
                    patient.delete_from_db()
                    patient.add_to_database()
                else:
                    return
            else:
                patient.add_to_database()
                
            messagebox.showinfo("Success", "Patient added successfully!")
            # Clear entry fields
            name_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)
            birth_date_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

            add_patient_window.destroy()

        # Wrapper frame para centralizar o conteúdo
        wrapper = ttk.Frame(add_patient_window, padding=10)
        wrapper.pack(fill="both", expand=True)

        # Configurar o grid do wrapper
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_columnconfigure(1, weight=1)
        wrapper.grid_columnconfigure(2, weight=1)
        wrapper.grid_rowconfigure(5, weight=1)

        # Name
        ttk.Label(wrapper, text="Name:").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(wrapper, width=30)
        name_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Address
        ttk.Label(wrapper, text="Address:").grid(row=1, column=1, padx=5, pady=5, sticky="e")
        address_entry = ttk.Entry(wrapper, width=30)
        address_entry.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Birth Date
        ttk.Label(wrapper, text="Birth Date:").grid(row=2, column=1, padx=5, pady=5, sticky="e")
        birth_date_entry = ttk.Entry(wrapper, width=30)
        birth_date_entry.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        from utils import format_date
        # Bind the formatting functions to the entries
        birth_date_entry.bind('<KeyRelease>', lambda e: format_date(e, birth_date_entry))
        
        # Phone
        ttk.Label(wrapper, text="Phone:").grid(row=3, column=1, padx=5, pady=5, sticky="e")
        phone_entry = ttk.Entry(wrapper, width=30)
        phone_entry.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # Email
        ttk.Label(wrapper, text="Email:").grid(row=4, column=1, padx=5, pady=5, sticky="e")
        email_entry = ttk.Entry(wrapper, width=30)
        email_entry.grid(row=4, column=2, padx=5, pady=5, sticky="w")

        # Botões
        confirm_button = ttk.Button(wrapper, text="Confirm", command=add_patient_to_db)
        confirm_button.grid(row=5, column=2, padx=5, pady=10, sticky="w")  # Alinhado à esquerda na mesma coluna

        cancel_button = ttk.Button(wrapper, text="Cancel", command=add_patient_window.destroy)
        cancel_button.grid(row=6, column=2, padx=5, pady=5, sticky="w")  # Alinhado à esquerda na mesma coluna

        # Prevenir redimensionamento dos widgets
        for row in range(7):
            wrapper.grid_rowconfigure(row, weight=0)

        # Ajustando o layout para que a janela e os campos de entrada possam ser redimensionados igualmente
        add_patient_window.grid_columnconfigure(0, weight=1, uniform="equal")
        add_patient_window.grid_columnconfigure(2, weight=1, uniform="equal")


        
