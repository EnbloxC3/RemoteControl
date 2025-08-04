from tkinter import messagebox
from threading import Thread
import threading

def show_message(message, type="info", ontop = 1):
    def _show():
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", bool(ontop))
        if type == "error":
            messagebox.showerror("Error", message, parent=root)
        elif type == "warning":
            messagebox.showwarning("Warning", message, parent=root)
        else:
            messagebox.showinfo("Message", message, parent=root)
        root.destroy()
    threading.Thread(target=_show).start()

if __name__ == "__main__":
    print("This module is not meant to be run directly.")