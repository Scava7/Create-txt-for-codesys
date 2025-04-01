import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import os

column_name_actual = 'default_value'
column_name_new = 'factory_value'

def scegli_file():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale
    file_path = filedialog.askopenfilename(
        title="Scegli un database SQLite",
        filetypes=[("Database SQLite", "*.db *.sqlite3"),("Database SQLite", "*.db *.sqlite"), ("Tutti i file", "*.*")]
    )
    return file_path

def rinomina_colonna(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelle = cursor.fetchall()

    modificate = []

    for (tabella,) in tabelle:
        cursor.execute(f"PRAGMA table_info('{tabella}')")
        colonne = cursor.fetchall()
        
        nomi_colonne = [col[1] for col in colonne]
        
        if column_name_actual in nomi_colonne:
            print(f"[INFO] Trovata colonna '{column_name_actual}' nella tabella '{tabella}'")
            nuova_tabella = f"{tabella}_temp"
            colonne_modificate = [(column_name_new if nome == column_name_actual else nome) for nome in nomi_colonne]
            
            # Ricrea la tabella con la colonna rinominata
            colonne_definizione = ", ".join(
                f'"{col[1] if col[1] != column_name_actual else column_name_new}" {col[2]}'
                for col in colonne
            )
            cursor.execute(f"CREATE TABLE {nuova_tabella} ({colonne_definizione})")

            # Copia i dati
            colonne_origine = ", ".join(f'"{nome}"' for nome in nomi_colonne)
            colonne_destinazione = ", ".join(f'"{nome}"' for nome in colonne_modificate)
            cursor.execute(f"""
                INSERT INTO {nuova_tabella} ({colonne_destinazione})
                SELECT {colonne_origine} FROM {tabella}
            """)

            # Rimuove la vecchia tabella e rinomina quella nuova
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
        tabelle_modificate = rinomina_colonna(path_db)
        if tabelle_modificate:
            msg = f"Colonna rinominata nelle tabelle: {', '.join(tabelle_modificate)}"
        else:
            msg = "Nessuna tabella conteneva la colonna '0'."
        messagebox.showinfo("Operazione completata", msg)
