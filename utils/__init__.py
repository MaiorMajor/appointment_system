import tkinter as tk


def get_id(value: str, type_of_value: str, table: str):
    """
    Retrieves the ID from a specified table based on a value and column name.

    Args:
        value (str): The value to search for in the specified column
        type_of_value (str): The column name to search in
        table (str): The name of the database table to query

    Returns:
        tuple: A tuple containing the ID if found, None otherwise
    """
    import sqlite3
    from constants import PATH_TO_DB

    # Define allowed tables and columns
    allowed_tables = {'users', 'consultations', 'doctor', 'patient'}  # Example table names
    allowed_columns = {'email', 'username', 'name'}  # Example column names

    # Validate table and column names
    if table not in allowed_tables:
        raise ValueError(f"Invalid table name: {table}")
    if type_of_value not in allowed_columns:
        raise ValueError(f"Invalid column name: {type_of_value}")

    with sqlite3.connect(PATH_TO_DB) as conn:
        cursor = conn.cursor()
        # Use string formatting for table and column names after validation
        query = f"SELECT id FROM {table} WHERE {type_of_value} = ?"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        return result[0]

    
    
def delete_consultation():
    pass


def create_user(email_entry, password_entry, is_admin_var, close_window=None, function_to_call=None):
    """
    Creates and saves a new user based on form input.

    Args:
        email_entry: Entry widget containing user's email
        password_entry: Entry widget containing user's password
        is_admin_var: BooleanVar indicating if user should be admin
    
    Creates User object with hashed password and saves to database.
    """
    import hashlib
    import tkinter.messagebox as messagebox
    # Get values from form
    email = email_entry.get()
    # Hash the password for security
    hashed_password = hashlib.sha256(password_entry.get().encode()).hexdigest()
    is_admin = is_admin_var.get() # True or False
    from classes.user import User
    try:
        # Create user object and save to database
        user = User(email, hashed_password, is_admin)
        success = user.insert_in_db()
        
        if success:
            # Show success message
            user_type = "Admin" if is_admin else "User"
            messagebox.showinfo("Success", f"{user_type} '{email}' added to database.")
            if close_window:
                function_to_call()
                close_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to add user to database.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create user: {str(e)}")


def close_window_deiconify(last_window, curr_window):
    last_window.deiconify()
    curr_window.destroy()

def consultation_exists(patient_id, doctor_id):
    """
    Checks if a consultation exists between a patient and a doctor.
    """
    import sqlite3
    from constants import PATH_TO_DB
    with sqlite3.connect(PATH_TO_DB) as conn:
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM consultations WHERE patient = ? AND doctor = ?"
        cursor.execute(query, (patient_id, doctor_id))
        result = cursor.fetchone()
        return result[0] > 0

def consultation_exists_by_id (id):
    """
    Checks if a consultation exists by its ID.
    """
    import sqlite3
    from constants import PATH_TO_DB
    with sqlite3.connect(PATH_TO_DB) as conn:
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM consultations WHERE id = ?"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result[0] > 0

'''def handle_cols_for_query(columns_selection:str, table_name:str):
    """
    Takes column selection for an sqlite3 query and formats it in case a JOIN is needed.
    
    Args:
        columns_selection (str): Comma-separated column names (e.g. "patient, doctor, date, time")
        table_name (str): Name of the table (e.g. "consultations")
        
    Returns:
        str: Formatted column selection with table alias (e.g. "c.patient, c.doctor, c.date, c.time")
    """
    if is_join:
        table_alias = table_name[0].lower()
        columns = [col.strip() for col in columns_selection.split(',')]
        formatted_cols = [f"{table_alias}.{col}" for col in columns]
        return ", ".join(formatted_cols)
    else:
        return columns_selection'''



def shrink(referenced_tables: list) -> list:
    """
    Consolidates a list of table-column references into a compressed format by grouping references to the same table.

    Args:
        referenced_tables (list): A list of lists where each inner list contains two elements:
                                [table_name (str), column_name (str)]
                                Example: [['specialization', 'spec_id'], ['specialization', 'name']]

    Returns:
        list: A list of lists where each inner list contains three elements:
              [table_name (str), reference_count (int), column_names (list)]
              The reference_count indicates how many columns reference this table
              Example: [['specialization', 2, ['spec_id', 'name']]]

    Example:
        Input: [['specialization', 'spec_id'], ['specialization', 'name'], ['specialization', 'date_created']]
        Output: [['specialization', 3, ['spec_id', 'name', 'date_created']]]
    """
    result = []
    for table, column in referenced_tables:
        found = False
        for entry in result:
            if entry[0] == table:
                entry[1] += 1
                entry[2].append(column)
                found = True
                break
        if not found:
            result.append([table, 1, [column]])
    return result


def test_shrink():
    # Test case 1: Multiple references to same table
    test_input1 = [['specialization', 'specialization_id']]
    expected1 = [['specialization', 1, ['specialization_id']]]
    assert shrink(test_input1) == expected1

    # Test case 2: References to different tables
    test_input2 = [['doctor', 'id'], ['specialization', 'name'], ['hospital', 'location']]
    expected2 = [['doctor', 1, ['id']], ['specialization', 1, ['name']], ['hospital', 1, ['location']]]
    assert shrink(test_input2) == expected2

    # Test case 3: Empty input
    test_input3 = []
    expected3 = []
    assert shrink(test_input3) == expected3

    # Test case 4: Single reference
    test_input4 = [['doctor', 'name']]
    expected4 = [['doctor', 1, ['name']]]
    assert shrink(test_input4) == expected4

    # Test case 5: Mixed multiple references
    test_input5 = [['doctor', 'id'], ['doctor', 'name'], ['specialization', 'type'], ['doctor', 'email']]
    expected5 = [['doctor', 3, ['id', 'name', 'email']], ['specialization', 1, ['type']]]
    assert shrink(test_input5) == expected5

    print("All tests passed!")

#test_shrink()

def get_foreign_keys(table_name: str) -> list:
    """
    Checks if a table has foreign keys and returns their information.
    
    Args:
        table_name (str): Name of the table to check
        
    Returns:
        list: List of dictionaries containing foreign key information
        Each dictionary contains:
            - from_col: Column in the current table
            - to_table: Referenced table
            - to_col: Referenced column
    """
    import sqlite3
    from constants import PATH_TO_DB
    
    with sqlite3.connect(PATH_TO_DB) as conn:
        cursor = conn.cursor()
        # Query to get foreign key information
        cursor.execute(f"""
            SELECT sql 
            FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        
        create_table_sql = cursor.fetchone()[0]
        
        # Get foreign key constraints
        cursor.execute(f"""
            SELECT * 
            FROM pragma_foreign_key_list(?)
        """, (table_name,))
        
        foreign_keys = []
        for fk in cursor.fetchall():
            foreign_keys.append({
                'from_col': fk[3],    # Column in current table
                'to_table': fk[2],    # Referenced table
                'to_col': fk[4]       # Referenced column
            })
            
        return foreign_keys

'''# Example usage:
fks = get_foreign_keys('consultations')
print(fks) # [{},{}] list of dicts
if fks:
    print("Foreign keys found:")
    for fk in fks:
        print(f"Column {fk['from_col']} references {fk['to_table']}.{fk['to_col']}")
else:
    print("No foreign keys found in this table")'''

def col_list_to_str(col_list: list) -> str:
    """
    Convert a list of column names to a comma-separated string.

    Args:
        col_list (list): List of column names

    Returns:
        str: Comma-separated string of column names.
    """
    return ', '.join(col.lower() for col in col_list)

#print(f"Get fk de doctor: {get_foreign_keys('doctor')}")

def build_query(table_name: str, columns: tuple) -> str:
    """
    Build an SQL query string for the given table and columns, handling foreign key relationships.

    This function constructs a SELECT query that automatically joins related tables based on foreign key
    relationships. It uses a predefined mapping of desired columns for specific tables and handles
    both simple queries and queries with foreign key relationships.

    Args:
        table_name (str): The name of the main table to query from
        columns (tuple): A tuple of column names to include in the SELECT statement

    Returns:
        str: A complete SQL query string with appropriate JOINs if foreign keys are present

    Example:
        >>> build_query("doctor", ("id", "name", "specialization_id"))
        'SELECT doctor.id, doctor.name, specialization.name FROM doctor JOIN specialization ON specialization.id = doctor.specialization_id'
    """
    # Define desired columns for specific tables
    desired_columns = {
        'specialization': 'name',
        'doctor': 'name',
        'patient': 'name'
    }

    # Retrieve foreign keys for the given table
    fks = get_foreign_keys(table_name)  # list of dicts which are all fks in table

    col_refs = []
    referenced_tables = {}

    # Build column references and track referenced tables
    for col in columns:
        fk = next((fk for fk in fks if fk['from_col'] == col), None)
        if fk:
            # Use the desired column from the mapping if available
            desired_col = desired_columns.get(fk['to_table'], fk['to_col'])
            col_refs.append(f"{fk['to_table']}.{desired_col}")
            if fk['to_table'] not in referenced_tables:
                referenced_tables[fk['to_table']] = []
            referenced_tables[fk['to_table']].append(fk['from_col'])
        else:
            col_refs.append(f"{table_name}.{col}")

    # Generate column list string
    columns_str = ', '.join(col_refs)

    # If no foreign keys are referenced
    if not referenced_tables:
        # Strip table prefixes for columns without foreign keys
        columns_str = ', '.join(col.replace(f"{table_name}.", "") for col in col_refs)
        return f"SELECT {columns_str} FROM {table_name}"

    # Start building the query
    query = f"SELECT {columns_str} FROM {table_name}"

    # Add JOINs for each referenced table
    for to_table, from_cols in referenced_tables.items():
        fk = next(fk for fk in fks if fk['to_table'] == to_table)
        query += f" JOIN {to_table} ON {to_table}.{fk['to_col']} = {table_name}.{from_cols[0]}"

    return query
       
def test_build_query():
    import inspect
    current_function = inspect.currentframe().f_code.co_name

    # Test case 1: Query with one foreign key
    print(build_query("doctor", ("id", "name", "email", "specialization_id")))
    print(build_query("doctor", ("id", "name", "email", "specialization_id")) == "SELECT doctor.id, doctor.name, doctor.email, specialization.name FROM doctor JOIN specialization ON specialization.id = doctor.specialization_id")

    # Test case 2: Simple query without foreign keys
    print(build_query("doctor", ("id", "name")))
    print(build_query("doctor", ("id", "name")) == "SELECT id, name FROM doctor")


    # Test case 3: Query with multiple foreign keys
    print(build_query("consultations", ("id", "patient", "doctor", "date", "time")))
    test_3 = build_query("consultations", ("id", "patient", "doctor", "date", "time")) == "SELECT consultations.id, patient.name, doctor.name, consultations.date, consultations.time FROM consultations JOIN doctor ON doctor.id = consultations.doctor JOIN patient ON patient.id = consultations.patient" 

    test_3_1 = build_query("consultations", ("id", "patient", "doctor", "date", "time")) == "SELECT consultations.id, patient.name, doctor.name, consultations.date, consultations.time FROM consultations JOIN patient ON patient.id = consultations.patient JOIN doctor ON doctor.id = consultations.doctor"
    print(test_3)
    print(test_3_1)

    # Test case 5: Single column
    print(build_query("patient", ("name",)))
    print(build_query("patient", ("name",)) == "SELECT name FROM patient")
    print(f"All test cases passed for {current_function}!")

#test_build_query()

def format_date(event, entry):
    """
    Formats and validates a date input in YYYY-MM-DD format.
    
    Args:
        event: The event that triggered the function
        entry: The tkinter Entry widget containing the date text
        
    Returns:
        'break' if the date is fully formatted, None otherwise
        
    The function enforces:
    - Maximum 8 digits (YYYYMMDD)
    - Valid months (01-12)
    - Valid days based on month and leap year rules
    - Automatically adds dashes when complete
    """
    text = entry.get().replace('-','')
    
    # Prevent more than 8 digits
    if len(text) > 8:
        entry.delete(8, tk.END)
        text = text[:8]
    
    # Format and validate month when entering 5th and 6th digits
    if len(text) == 5:
        month_first_digit = text[4]
        if int(month_first_digit) > 1:
            text = text[:4] + '1' + text[5:]
            entry.delete(0, tk.END)
            entry.insert(0, text)
    
    if len(text) == 6:
        month = text[4:6]
        if month.startswith('0') and month[1] == '0':
            text = text[:5] + '1' + text[6:]
        elif month.startswith('1') and int(month[1]) > 2:
            text = text[:5] + '2' + text[6:]
        entry.delete(0, tk.END)
        entry.insert(0, text)
    
    # Format and validate days when entering 7th and 8th digits
    if len(text) == 7:
        day_first_digit = text[6]
        if int(day_first_digit) > 3:
            text = text[:6] + '3' + text[7:]
            entry.delete(0, tk.END)
            entry.insert(0, text)
    
    if len(text) == 8:
        day = text[6:8]
        month = text[4:6]
        
        # Get max days for the month
        if month in ['04', '06', '09', '11']:
            max_days = 30
        elif month == '02':
            year = int(text[:4])
            # Check for leap year
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                max_days = 29
            else:
                max_days = 28
        else:
            max_days = 31
            
        # Validate day value
        day_num = int(day)
        if day_num > max_days:
            day = str(max_days)
            text = text[:6] + day
            
        # Format final date with dashes
        formatted = f"{text[:4]}-{text[4:6]}-{text[6:]}"
        entry.delete(0, tk.END)
        entry.insert(0, formatted)
        return 'break'

def format_time(event, entry):
    """
    Formats and validates a time input in HH:MM format.
    
    Args:
        event: The event that triggered the function
        entry: The tkinter Entry widget containing the time text
        
    Returns:
        'break' if the time is fully formatted, None otherwise
        
    The function enforces:
    - Maximum 4 digits (HHMM)
    - Valid hours (00-23)
    - Valid minutes (00-59)
    - Automatically adds colon when complete
    """
    text = entry.get().replace(':','')
    
    # Prevent more than 4 digits
    if len(text) > 4:
        entry.delete(4, tk.END)
        text = text[:4]
    
    # Validate first hour digit
    if len(text) == 1:
        if int(text[0]) > 2:
            text = '2'
            entry.delete(0, tk.END)
            entry.insert(0, text)
    
    # Validate second hour digit
    if len(text) == 2:
        hours = text[:2]
        if hours.startswith('2') and int(hours[1]) > 3:
            text = '23'
        entry.delete(0, tk.END)
        entry.insert(0, text)
    
    # Validate first minute digit
    if len(text) == 3:
        if int(text[2]) > 5:
            text = text[:2] + '5'
            entry.delete(0, tk.END)
            entry.insert(0, text)
    
    # Format final time with validation
    if len(text) == 4:
        minutes = text[2:]
        if int(minutes) > 59:
            minutes = '59'
        formatted = f"{text[:2]}:{minutes}"
        entry.delete(0, tk.END)
        entry.insert(0, formatted)
        return 'break'