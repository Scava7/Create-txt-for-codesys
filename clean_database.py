import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import re

def scegli_db():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Seleziona il database da pulire",
        filetypes=[("Database SQLite", "*.db *.sqlite"), ("Tutti i file", "*.*")]
    )

def pulisci_stringa(val):
    if isinstance(val, str):
        val = val.strip()
        val = re.sub(r'\s+', ' ', val)
    return val

def pulisci_database(path_originale):
    path_pulito = os.path.splitext(path_originale)[0] + "_cleaned.sqlite"
    shutil.copy(path_originale, path_pulito)

    conn = sqlite3.connect(path_pulito)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelle = [row[0] for row in cursor.fetchall()]

    for tabella in tabelle:
        print(f"[INFO] Pulizia tabella: {tabella}")
        df = pd.read_sql_query(f'SELECT rowid, * FROM "{tabella}"', conn)

        colonne_da_pulire = [col for col in df.columns if df[col].dtype == object and col != "rowid"]
        if not colonne_da_pulire:
            continue

        for col in colonne_da_pulire:
            df[col] = df[col].apply(pulisci_stringa)

        for idx, row in df.iterrows():
            set_clause = ", ".join([f'"{col}" = ?' for col in colonne_da_pulire])
            values = [row[col] for col in colonne_da_pulire]
            pk = row["rowid"]
            cursor.execute(f"""
                UPDATE "{tabella}"
                SET {set_clause}
                WHERE rowid = ?;
            """, values + [pk])

        conn.commit()

    conn.close()
    print(f"[OK] Database pulito salvato come: {path_pulito}")
    messagebox.showinfo("Operazione completata", f"Database pulito salvato come:\n{path_pulito}")

# --- MAIN ---
if __name__ == "__main__":
    path = scegli_db()
    if not path:
        print("Nessun file selezionato.")
    elif not os.path.exists(path):
        print("File non trovato.")
    else:
        pulisci_database(path)
