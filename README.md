# MedCare Health Center - School Project

MedCare Health Center is a desktop application developed in Python using Tkinter for the graphical user interface and SQLite3 for data persistence.  This project simulates a health center management system, focusing on user authentication, consultation management, and administrative functionalities.

## Project Structure

The project is organized into the following directories and files:

├── assets/
│   └── images/
│       ├── file-removebg-preview.png (Company Logo)
├── classes/
│   ├── person.py     (Base class for Person)
│   ├── patient.py    (Patient class)
│   ├── doctor.py     (Doctor class)
│   ├── user.py      (User authentication)
│   └── table.py      (Consultation table UI)
├── database/
│   └── create_db.py   (Database operations)
├── └── clinic.db      (Database file)
├── constants/
│   └── __init__.py   (Constants)
├── gui/
│   ├── first_window.py (Initial window)
│   ├── login_window.py (Login interface)
│   ├── menu_admin.py (Admin menu)
│   └── menu.py       (Main menu)
├── utils/
│   └── __init__.py   (Utility functions)
├── main.py           (Main application entry point)
└── README.md          (This file)


## Core Functionalities

### User Authentication

- Secure user authentication with SHA256 password hashing.
- Different user roles (admin and regular user) with distinct access privileges.

### Consultation Management

- **View:** Consultations displayed in a sortable table (newest first), showing doctor, specialization, patient, and date/time.
- **Add:**  New consultations can be scheduled.  (Implementation details to be added during presentation)
- **Edit:** Existing consultation details (doctor, patient, date, time) can be modified.
- **Delete:** Consultations can be removed. (Implementation details to be added during presentation)

### Admin Panel

- **User Management:** Search, add, and delete users.
- **Doctor Management:** Search, add, and delete doctors.
- **Specialization Management:** Search, add, and delete specializations (Implementation details to be added during presentation).
- **Patient Records Management:**  (Implementation details to be added during presentation)


## Technologies Used

- **Python:** Primary programming language.
- **Tkinter:**  GUI framework for creating the user interface.
- **SQLite3:**  Database for storing user data, consultations, doctors, and patients.
- **Hashlib (SHA256):**  Used for secure password hashing.