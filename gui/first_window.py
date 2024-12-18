import tkinter as tk
from tkinter import ttk
from constants import PATH_TO_IMAGES
import utils

class FirstWindow:
    """The `FirstWindow` class represents the main window of the Health Center application. It sets up the initial window, including the application title, size, and a main frame. The class also loads and displays the company logo, and creates a login button that opens the login window when clicked."""
    def __init__(self, root):
        self.root = root
        self.root.title("MedCare Health Center")
        self.root.geometry("400x400")
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure main frame grid weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Load and display company logo
        self.logo_image = tk.PhotoImage(file=PATH_TO_IMAGES+"\\file-removebg-preview.png")
        self.logo_label = ttk.Label(self.main_frame, image=self.logo_image)
        self.logo_label.grid(row=0, column=0, pady=20)
        
        # Login button
        self.login_button = ttk.Button(self.main_frame, text="Login", command=self.open_login)
        self.login_button.grid(row=1, column=0, pady=20)


    def open_login(self):
        self.main_frame.destroy()
        from gui.login_window import LoginWindow
        LoginWindow(self.root)


