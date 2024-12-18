import tkinter as tk
from tkinter import ttk
import sqlite3
from constants import PATH_TO_DB
from datetime import datetime

class ConsultationTable:
    """
    The `ConsultationTable` class is responsible for creating and managing a table-like UI component to display a list of consultations. It uses the Tkinter library to create the GUI elements and the SQLite database to fetch the consultation data.

    The class has the following main responsibilities:
    - Create a LabelFrame to hold the table UI components
    - Create a Treeview widget to display the consultation data
    - Configure the column headings and widths of the Treeview
    - Add a vertical scrollbar to the Treeview
    - Load the consultation data from the SQLite database and populate the Treeview
    """
    def __init__(self, parent):
        self.parent = parent
        # Create LabelFrame
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Create treeview
        self.table = ttk.Treeview(self.frame, columns=("Doctor", "Specialization", "Patient", "Date and Time"), show="headings")
        self.table.heading("Doctor", text="Doctor")
        self.table.heading("Specialization", text="Specialization")
        self.table.heading("Patient", text="Patient")
        self.table.heading("Date and Time", text="Date and Time")
        
        # Scrollbars for the table
        scrollbar_y = ttk.Scrollbar(
            self.frame, 
            orient="vertical", 
            command=self.table.yview
            )
        scrollbar_x = ttk.Scrollbar(
            self.frame, 
            orient="horizontal", 
            command=self.table.xview
            )
        self.table.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Layout for the table and scrollbars
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Load data
        self.load_appointments()

    
    def load_appointments(self):
        try:
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                # This query fetches all consultations sorted by date and time
                query = """
                    SELECT c.id, d.name, s.name, p.name, c.date || ' ' || c.time
                    FROM consultations c
                    JOIN doctor d ON c.id = d.id
                    JOIN specialization s ON d.specialization_id = s.id
                    JOIN patient p ON c.id = p.id
                    ORDER BY c.date, c.time
                """
                #print("Executing query:", query)
                cursor.execute(query)
                rows = cursor.fetchall()
                #print("Retrieved rows:", rows)
                
                # Clear existing items
                for item in self.tree.get_children():
                    self.table.delete(item)
                    
                # Insert new data
                for row in rows:
                    self.table.insert('', 'end', values=row)
                    #print("Inserted row:", row)
                    
        except sqlite3.Error as e:
            print("Database error:", e)