import tkinter as tk
from tkinter import filedialog, messagebox
import os


def scegli_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Scegli un database SQLite",
        filetypes=[("Database SQLite", "*.db *.sqlite3"),("Database SQLite", "*.db *.sqlite") , ("Tutti i file", "*.*")]
    )