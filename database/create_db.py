import sqlite3
import hashlib

# Create a connection to the database
conn = sqlite3.connect('database/clinic.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS patient (
    id INTEGER PRIMARY KEY, -- citizen card number
    name TEXT NOT NULL,
    address TEXT,
    birth_date DATE,
    phone TEXT,
    email TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS specialization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctor (
    id INTEGER PRIMARY KEY, -- doctor credential number
    name TEXT NOT NULL,
    email TEXT,
    specialization_id INTEGER,
    FOREIGN KEY (specialization_id) REFERENCES specialization(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS consultations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient INTEGER,
    doctor INTEGER,
    date DATE,
    time TIME,
    FOREIGN KEY (patient) REFERENCES patient(id),
    FOREIGN KEY (doctor) REFERENCES doctor(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
)
''')

# Insert default data into the users table
cursor.execute('''
INSERT INTO users (email, password)
VALUES 
    ('alice@domain.com', ?),
    ('bob@domain.com', ?),
    ('charlie@domain.com', ?)
''', (
    hashlib.sha256('alice123'.encode()).hexdigest(),
    hashlib.sha256('bob123'.encode()).hexdigest(),
    hashlib.sha256('charlie123'.encode()).hexdigest()
))

# Insert admin user with encryption
password = input("Enter the password for the admin1 user: ")
hashed_password = hashlib.sha256(password.encode()).hexdigest()
cursor.execute('''
               INSERT INTO users (email, password, is_admin)
               VALUES ('admin1', ?, 1)
               ''', (hashed_password,)) # admin1
password = input("Enter the password for the admin2 user: ")
hashed_password = hashlib.sha256(password.encode()).hexdigest()
cursor.execute('''
               INSERT INTO users (email, password, is_admin)
               VALUES ('admin2', ?, 1)
               ''', (hashed_password,)) #admin2

# Insert data into specialization table
cursor.execute('''
INSERT INTO specialization (name)
VALUES 
    ('General Practice'),
    ('Pediatrics'),
    ('Neurology'),
    ('Oncology'),
    ('Psychiatry'),
    ('Radiology'),
    ('Orthopedics'),
    ('Cardiology'),
    ('Gastrentrology')
''')

# Insert data into patient table
cursor.execute('''
INSERT INTO patient (name, address, birth_date, phone, email)
VALUES 
    ('João Silva', 'Rua A, 123', '1980-01-01', '912345678', 'joao@email.com'),
    ('Maria Santos', 'Rua B, 456', '1990-05-15', '923456789', 'maria@email.com'),
    ('Pedro Costa', 'Rua C, 789', '1975-12-30', '934567890', 'pedro@email.com'),
    ('Marco André', 'Rua D, 148', '1993-06-06', '919293949', 'marco@email.com'),
    ('José Fernandes', 'Rua E, 284', '1998-08-18', '929394959', 'jose@email.com'),
    ('Ana Ferreira', 'Rua F, 391', '1987-02-22', '939495969', 'ana@email.com'),
    ('Marta Chaves', 'Rua G, 426', '1984-05-25', '912934956', 'marta@email.com'),
    ('Fernando Marques', 'Rua H, 590', '2009-04-12', '923945967', 'fernando@email.com')
''')

# Insert data into doctor table
cursor.execute('''
INSERT INTO doctor (name, email, specialization_id)
VALUES 
    ('Dr. Carlos Oliveira', 'carlos@clinica.com', 1),
    ('Dra. Ana Pereira', 'ana@clinica.com', 2),
    ('Dr. Ricardo Santos', 'ricardo@clinica.com', 3),
    ('Dr. Alexandre Ferreira', 'alexandre@clinica.com', 4),
    ('Dr. Diogo Vieira', 'diogo@clinica.com', 5),
    ('Dra. Maria Nunes', 'maria@clinica.com', 6),
    ('Dra. Inês Pereira', 'ines@clinica.com', 7),
    ('Dr. Álvaro Camarinha', 'alvaro@clinica.com', 8),
    ('Dr. Cuca Beludo', 'cuca@clinica.com', 9)
''')

# Insert data into consultations table
cursor.execute('''
INSERT INTO consultations (patient, doctor, date, time)
VALUES 
    (1, 1, '2024-01-15', '09:00'),
    (2, 2, '2024-01-15', '09:30'),
    (3, 3, '2024-01-15', '10:00'),
    (4, 4, '2024-12-02', '09:00'),
    (5, 5, '2024-12-02', '09:30'),
    (6, 6, '2024-12-02', '11:30'),
    (7, 7, '2024-12-02', '16:30'),
    (8, 8, '2024-12-02', '13:30')
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
