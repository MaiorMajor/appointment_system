import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from gui.first_window import FirstWindow
from gui.menu import Menu


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MedCare Login")
        
        self._create_main_frame()
        self._create_login_widgets()
        self.root.bind('<Return>', lambda event: self.check_login())
    
    def _create_main_frame(self):
        # Create main frame for login
        self.login_frame = ttk.Frame(self.root, padding="10")
        self.login_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def _create_login_widgets(self):
        # Create login widgets
        self.label_user = ttk.Label(self.login_frame, text="E-mail:")
        self.label_user.pack(pady=5)
        self.entry_user = ttk.Entry(self.login_frame)
        self.entry_user.pack(pady=5, padx=20)

        self.label_password = ttk.Label(self.login_frame, text="Password:")
        self.label_password.pack(pady=5)
        self.entry_password = ttk.Entry(self.login_frame, show="*")
        self.entry_password.pack(pady=5, padx=20)
        self.button_login = ttk.Button(self.login_frame, text="Login", command=self.check_login)
        self.button_login.pack(pady=10)
        
    def check_login(self):
        """Validates credentials and changes layout if login is successful."""
        email = self.entry_user.get()
        
        from hashlib import sha256
        password = sha256(self.entry_password.get().encode()).hexdigest()

        from classes.user import User
        user = User(email, password)
        
        if user.exists_in_db():
            messagebox.showinfo("Login Successful", f"Welcome {email}!")
            self.login_frame.destroy()
            from gui.menu import Menu
            Menu(self.root, admin=user.is_admin())
        else:
            messagebox.showerror("Error", "Invalid credentials. Try again.")