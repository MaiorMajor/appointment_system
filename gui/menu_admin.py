from gui.menu import Menu
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constants import *

class AdminMenu(Menu):
    def __init__(self, root):
        super().__init__(root)
        self.root.withdraw()
        self.admin_window = tk.Toplevel()
        self.admin_window.title("Admin Menu")
        self.admin_window.geometry("300x200")
        manage_list = [
            ["Users", USERS_COLUMNS_IN_DB],
            ["Doctor", DOCTORS_COLUMNS_IN_DB],
            ["Specialization", SPECIALIZATIONS_COLUMNS_IN_DB]
        ]
        for i in range(len(manage_list)):
            item = manage_list[i]  # Create a local variable for each iteration
            ttk.Button(
                self.admin_window,
                text=f"Manage {item[0]}",
                command=lambda item=item: self.manage(item[0], item[1])
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=10,
                sticky="ew"
            )
        
        from utils import close_window_deiconify
        ttk.Button(
            self.admin_window, 
            text="Return to Main Menu", 
            command=lambda: close_window_deiconify(
                self.root, 
                self.admin_window
                )
            ).grid(
                row=3, 
                column=0, 
                padx=10, 
                pady=10, 
                sticky="ew"
                )

    
    def search_items(self, table_name: str, col_list: tuple, search_entry: tk.Entry, tree: ttk.Treeview):
        """
        Generic search method for any table.
        
        Args:
            table_name (str): Name of the table to search in
            col_list (tuple): List of columns to search through
            search_entry (tk.Entry): Entry widget containing search query
            tree (ttk.Treeview): Treeview to display results
        """
        query = search_entry.get().lower().replace("'", "''")  # Escape single quotes
        if query == "press enter to search...":
            return

        # Clear current treeview
        for item in tree.get_children():
            tree.delete(item)

        import sqlite3
        from constants import PATH_TO_DB
        from utils import build_query
        
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            # Build base query
            select_query = build_query(table_name, col_list)
            
            # Add WHERE clause for searching across all columns
            where_clauses = []
            for col in col_list:
                # Prefix the column names with table name to avoid ambiguity
                table_prefix = table_name + "."
                if "." not in col:  # Only add prefix if not already prefixed
                    where_clauses.append(f"{table_prefix}{col} LIKE '%{query}%'")
                else:
                    where_clauses.append(f"{col} LIKE '%{query}%'")
            
            if where_clauses:
                select_query += " WHERE " + " OR ".join(where_clauses)
            print(f"Executing query: {select_query}")
            cursor.execute(select_query)
            for row in cursor.fetchall():
                tree.insert('', tk.END, values=row)

    def manage(self, type:str, col_list:tuple):
        """
        Creates and manages a window for handling database records.
        
        Args:
            type (str): The type of records to manage (e.g., "Specialties", "Doctors")
            col_list (tuple): Tuple of column names to display in the treeview
        """
        self.manage_window = tk.Toplevel()
        self.manage_window.title("Manage " + type)
        self.manage_window.geometry("800x600")

        # Configure grid weights
        self.manage_window.grid_columnconfigure(0, weight=1)
        self.manage_window.grid_columnconfigure(1, weight=1)
        self.manage_window.grid_rowconfigure(1, weight=1)

        # Search functionality
        search_label = ttk.Label(self.manage_window, text="Search:")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        search_entry = ttk.Entry(self.manage_window)
        search_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Create Treeview
        self.tree = ttk.Treeview(self.manage_window, columns=col_list, show='headings')
        for col in col_list:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.manage_window, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid layout
        self.tree.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        scrollbar.grid(row=1, column=2, sticky='ns')

        # Get selected items function
        def get_selected_items():
            selected_items = self.tree.selection()
            if selected_items:
                return [self.tree.item(item)['values'] for item in selected_items]
            return None

        # Button frame
        button_frame = ttk.Frame(self.manage_window)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Add buttons
        ttk.Button(
            button_frame, 
            text=f"Add {type}", 
            command=lambda: self.add_item(type, col_list)
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame, 
            text=f"Edit {type}", 
            command=lambda: self.edit_item(type, col_list, get_selected_items())
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame, 
            text=f"Delete {type}", 
            command=lambda: self.delete_item(type, get_selected_items(), col_list)
        ).grid(row=0, column=2, padx=5)

        # Add search functionality
        search_entry.insert(0, "Press Enter to Search...")
        search_entry.configure(foreground='grey')

        def on_focus_in(event):
            if search_entry.get() == "Press Enter to Search...":
                search_entry.delete(0, "end")
                search_entry.configure(foreground='black')

        def on_focus_out(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Press Enter to Search...")
                search_entry.configure(foreground='grey')

        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        search_entry.bind('<Return>', 
            lambda event: self.search_items(type.lower(), col_list, search_entry, self.tree)
        )

        # Initial data load
        self.load_data(type, col_list, search_entry, self.tree)


    def add_item(self, type: str, col_list: tuple):
        """Generic method to add items to any table"""
        add_window = tk.Toplevel()
        add_window.title(f"Add {type}")
        add_window.geometry("400x400")
        
        # Create entry fields dynamically based on columns
        entries = {}
        for i, col in enumerate(col_list[1:], 1):  # Skip ID column
            ttk.Label(add_window, text=f"{col}:").grid(row=i-1, column=0, padx=5, pady=5)
            if col.lower() == 'password':
                entries[col] = ttk.Entry(add_window, show='*')
            elif col.lower() == 'is_admin':
                entries[col] = tk.BooleanVar()
                checkbox = ttk.Checkbutton(add_window, variable=entries[col])
                checkbox.grid(row=i-1, column=1, padx=5, pady=5)
                continue
            elif col.lower() == 'specialization_id':
                # Create a combobox for specializations
                entries[col] = ttk.Combobox(add_window, state='readonly')
                # Fetch specializations from database
                import sqlite3
                from constants import PATH_TO_DB
                with sqlite3.connect(PATH_TO_DB) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, name FROM specialization")
                    specializations = cursor.fetchall()
                # Store the id-name mapping for later use
                entries[f"{col}_mapping"] = {spec[1]: spec[0] for spec in specializations}
                # Show only the names in the dropdown
                entries[col]['values'] = list(entries[f"{col}_mapping"].keys())
            else:
                entries[col] = ttk.Entry(add_window)
            entries[col].grid(row=i-1, column=1, padx=5, pady=5)
        
        def save():
            values = []
            import hashlib
            for col in col_list[1:]:
                if col.lower() == 'password':
                    password = entries[col].get()
                    if password:
                        hashed = hashlib.sha256(password.encode()).hexdigest()
                        values.append(hashed)
                    else:
                        values.append('')
                elif col.lower() == 'is_admin':
                    values.append(1 if entries[col].get() else 0)
                elif col.lower() == 'specialization_id':
                    selected_name = entries[col].get()
                    values.append(entries[f"{col}_mapping"][selected_name])
                else:
                    values.append(entries[col].get())
                    
            if not all(str(v) for v in values):
                messagebox.showerror("Error", "Please fill all fields")
                return
                
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                placeholders = ','.join(['?' for _ in col_list[1:]])
                cursor.execute(
                    f"INSERT INTO {type.lower()} ({','.join(col_list[1:])}) VALUES ({placeholders})",
                    values
                )
            
            messagebox.showinfo("Success", f"{type} added successfully!")
            add_window.destroy()
            self.load_data(type, col_list, None, self.tree)

        ttk.Button(add_window, text="Save", command=save).grid(row=len(col_list), column=0, columnspan=2, pady=10)

    def edit_item(self, type: str, col_list: tuple, selection):
        """Generic method to edit items in any table"""
        if not selection or len(selection) != 1:
            messagebox.showwarning("Warning", "Please select exactly one item to edit")
            return
            
        edit_window = tk.Toplevel()
        edit_window.title(f"Edit {type}")
        edit_window.geometry("400x400")
        
        # Create entry fields with current values
        entries = {}
        password_entry = None  # Store reference to password entry
        row_counter = 0
        for i, col in enumerate(col_list[1:], 1):  # Skip ID column
            ttk.Label(edit_window, text=f"{col}:").grid(row=row_counter, column=0, padx=5, pady=5)
            if col.lower() == 'password':
                password_entry = ttk.Entry(edit_window, show='*', state='disabled')
                password_entry.insert(0, selection[0][i])
                password_entry.grid(row=row_counter, column=1, padx=5, pady=5)
                entries[col] = password_entry
                
                def reset_password():
                    password_entry.config(state='normal')
                    password_entry.delete(0, 'end')
                
                ttk.Button(edit_window, text="Reset Password", command=reset_password).grid(row=row_counter+1, column=1, padx=5, pady=2)
                row_counter += 2
            elif col.lower() == 'is_admin':
                entries[col] = tk.BooleanVar(value=bool(selection[0][i]))
                checkbox = ttk.Checkbutton(edit_window, variable=entries[col])
                checkbox.grid(row=row_counter, column=1, padx=5, pady=5)
                row_counter += 1
            elif col.lower() == 'specialization_id':
                # Create a combobox for specializations
                entries[col] = ttk.Combobox(edit_window, state='readonly')
                # Fetch specializations from database
                import sqlite3
                from constants import PATH_TO_DB
                with sqlite3.connect(PATH_TO_DB) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, name FROM specialization")
                    specializations = cursor.fetchall()
                # Store the id-name mapping for later use
                entries[f"{col}_mapping"] = {spec[1]: spec[0] for spec in specializations}
                entries[f"{col}_reverse_mapping"] = {spec[0]: spec[1] for spec in specializations}
                # Show only the names in the dropdown
                entries[col]['values'] = list(entries[f"{col}_mapping"].keys())
                # Set current value
                current_spec_name = entries[f"{col}_reverse_mapping"].get(selection[0][i], selection[0][i])
                entries[col].set(current_spec_name)
                entries[col].grid(row=row_counter, column=1, padx=5, pady=5)
                row_counter += 1
            else:
                entries[col] = ttk.Entry(edit_window)
                entries[col].insert(0, selection[0][i])
                entries[col].grid(row=row_counter, column=1, padx=5, pady=5)
                row_counter += 1
        
        def save():
            values = []
            import hashlib
            for col in col_list[1:]:
                if col.lower() == 'password':
                    password = entries[col].get()
                    if entries[col]['state'] == 'disabled':
                        values.append(password)  # Keep existing password hash
                    elif password:
                        hashed = hashlib.sha256(password.encode()).hexdigest()
                        values.append(hashed)
                    else:
                        values.append('')
                elif col.lower() == 'is_admin':
                    values.append(1 if entries[col].get() else 0)
                elif col.lower() == 'specialization_id':
                    selected_name = entries[col].get()
                    values.append(entries[f"{col}_mapping"][selected_name])
                else:
                    values.append(entries[col].get())
            
            values.append(selection[0][0])  # Add ID for WHERE clause
            
            if not all(str(v) for v in values[:-1]):  # Check all except ID
                messagebox.showerror("Error", "Please fill all fields")
                return
                
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                set_clause = ','.join([f"{col}=?" for col in col_list[1:]])
                cursor.execute(
                    f"UPDATE {type.lower()} SET {set_clause} WHERE id=?",
                    values
                )
            
            messagebox.showinfo("Success", f"{type} updated successfully!")
            edit_window.destroy()
            self.load_data(type, col_list, None, self.tree)

        ttk.Button(edit_window, text="Save", command=save).grid(row=row_counter, column=0, columnspan=2, pady=10)    
    
    def delete_item(self, type: str, selection, col_list: tuple):
        """Generic method to delete items from any table"""
        try:
            if not selection:
                messagebox.showwarning("Warning", "Please select items to delete")
                return
                    
            if not messagebox.askyesno("Confirm", f"Are you sure you want to delete {len(selection)} {type}(s)?"):
                return
                    
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                for item in selection:
                    if type.lower() == 'specialization':
                        # First get all doctors with this specialization
                        cursor.execute("SELECT id FROM doctor WHERE specialization_id=?", (item[0],))
                        doctor_ids = cursor.fetchall()
                        # Delete consultations for these doctors
                        for doctor_id in doctor_ids:
                            cursor.execute("DELETE FROM consultations WHERE doctor=?", (doctor_id[0],))
                        # Delete the doctors
                        cursor.execute("DELETE FROM doctor WHERE specialization_id=?", (item[0],))
                        # Finally delete the specialization
                        cursor.execute("DELETE FROM specialization WHERE id=?", (item[0],))
                    elif type.lower() == 'doctor':
                        # First delete all consultations for this doctor
                        cursor.execute("DELETE FROM consultations WHERE doctor=?", (item[0],))
                        # Then delete the doctor
                        cursor.execute("DELETE FROM doctor WHERE id=?", (item[0],))
                    else:
                        cursor.execute(f"DELETE FROM {type.lower()} WHERE id=?", (item[0],))
            
            messagebox.showinfo("Success", f"{len(selection)} {type}(s) deleted successfully!")
            self.load_data(type, col_list, None, self.tree)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Cannot delete: item is referenced by other records")

    def load_data(self, table_name:str, col_list:tuple, search_entry:tk.Entry, tree:ttk.Treeview):
        print(f"Loading data for table: {table_name}")
        print(f"Columns: {col_list}")
        table_name = table_name.lower()
        print(f"Loading data for table: {table_name}")

        # Clear existing items first
        for item in tree.get_children():
            tree.delete(item)
            
        import sqlite3
        from constants import PATH_TO_DB
        from utils import build_query
        
        try:
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                select_query = build_query(table_name, col_list)
                print(f"Executing query: {select_query}")
                
                cursor.execute(select_query)
                data = cursor.fetchall()
                print(f"Fetched {len(data)} rows")
                
                for row in data:
                    print(f"Inserting row: {row}")
                    tree.insert('', tk.END, values=row)
                    
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Failed to load data: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
