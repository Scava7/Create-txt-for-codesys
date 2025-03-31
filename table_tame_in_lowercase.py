import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def scegli_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Scegli un database SQLite",
        filetypes=[("Database SQLite", "*.db *.sqlite3"),("Database SQLite", "*.db *.sqlite"), ("Tutti i file", "*.*")]
    )

def rinomina_tabelle_lowercase(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Prende tutti i nomi delle tabelle
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelle = [row[0] for row in cursor.fetchall()]

    rinominate = []

    for nome_vecchio in tabelle:
        nome_nuovo = nome_vecchio.lower()

        if nome_vecchio == nome_nuovo:
            continue  # Già lowercase

        print(f"[INFO] Rinominando tabella '{nome_vecchio}' -> '{nome_nuovo}'")

        # Ottieni nomi colonne
        cursor.execute(f"PRAGMA table_info('{nome_vecchio}')")
        colonne = [col[1] for col in cursor.fetchall()]
        colonne_str = ", ".join(f'"{c}"' for c in colonne)

        # Crea nuova tabella
        cursor.execute(f"CREATE TABLE {nome_nuovo} AS SELECT * FROM '{nome_vecchio}'")

        # Elimina quella vecchia
        cursor.execute(f"DROP TABLE '{nome_vecchio}'")

        rinominate.append(f"{nome_vecchio} → {nome_nuovo}")
        conn.commit()

    conn.close()
    return rinominate

if __name__ == "__main__":
    path = scegli_file()
    if not path:
        print("Nessun file selezionato.")
    elif not os.path.exists(path):
        print("File non trovato.")
    else:
        tabelle_rinominate = rinomina_tabelle_lowercase(path)
        if tabelle_rinominate:
            msg = "Tabelle rinominate:\n" + "\n".join(tabelle_rinominate)
        else:
            msg = "Tutte le tabelle erano già in lowercase."
        messagebox.showinfo("Operazione completata", msg)
