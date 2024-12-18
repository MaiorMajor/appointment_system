import tkinter as tk

from gui.first_window import FirstWindow

def main():                     
    root = tk.Tk()  
    FirstWindow(root)       
    root.mainloop()
    

if __name__ == "__main__":
    main()