import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def scegli_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Scegli un database SQLite",
        filetypes=[("Database SQLite", "*.db *.sqlite3"), ("Database SQLite", "*.db *.sqlite"), ("Tutti i file", "*.*")]
    )
    return file_path

def colonne_lowercase(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelle = cursor.fetchall()

    modificate = []

    for (tabella,) in tabelle:
        cursor.execute(f"PRAGMA table_info('{tabella}')")
        colonne = cursor.fetchall()

        vecchi_nomi = [col[1] for col in colonne]
        nuovi_nomi = [col.lower() for col in vecchi_nomi]

        # Salta se già tutto in minuscolo
        if vecchi_nomi == nuovi_nomi:
            continue

        print(f"[INFO] Rinomino colonne in '{tabella}'")

        nuova_tabella = f"{tabella}_temp"

        # Ricrea la tabella con nomi in lowercase e stessi tipi
        colonne_definizione = ", ".join(
            f'"{nuovo}" {col[2]}' for nuovo, col in zip(nuovi_nomi, colonne)
        )
        cursor.execute(f"CREATE TABLE {nuova_tabella} ({colonne_definizione})")

        # Copia i dati
        vecchi = ", ".join(f'"{nome}"' for nome in vecchi_nomi)
        nuovi = ", ".join(f'"{nome}"' for nome in nuovi_nomi)
        cursor.execute(f"""
            INSERT INTO {nuova_tabella} ({nuovi})
            SELECT {vecchi} FROM {tabella}
        """)

        # Sostituisci la tabella
        cursor.execute(f"DROP TABLE {tabella}")
        cursor.execute(f"ALTER TABLE {nuova_tabella} RENAME TO {tabella}")
        conn.commit()

        modificate.append(tabella)

    conn.close()
    return modificate

if __name__ == "__main__":
    path_db = scegli_file()
    if not path_db:
        print("Nessun file selezionato.")
    elif not os.path.exists(path_db):
        print("Il file selezionato non esiste.")
    else:
        tabelle_modificate = colonne_lowercase(path_db)
        if tabelle_modificate:
            msg = f"Colonne trasformate in lowercase nelle tabelle: {', '.join(tabelle_modificate)}"
        else:
            msg = "Tutte le colonne erano già in lowercase. Nessuna modifica fatta."
        messagebox.showinfo("Operazione completata", msg)
