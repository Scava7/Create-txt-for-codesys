import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def scegli_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Scegli un database SQLite",
        filetypes=[("Database SQLite", "*.db *.sqlite3"), ("Database SQLite", "*.db *.sqlite"), ("Tutti i file", "*.*")]
    )

def genera_file_txt(db_path, nome_tabella, output_path):
    # Connessione al DB
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
    conn.close()

    # Prepara colonne formattate
    df["group_fmt"] = df["group"].apply(lambda g: f"(*{g}*)")
    df["global_variable_fmt"] = df["global_variable"].apply(lambda g: f"{g};")
    df["description"] = df["description"].fillna("")

    # Calcola le larghezze massime per ogni colonna
    max_len_group   = df["group_fmt"].str.len().max()
    max_len_exch    = df["exchange_variable"].str.len().max()
    max_len_global  = df["global_variable"].str.len().max()

    # Funzione per formattare ogni riga
    def formatta_riga(row):
        group = row['group_fmt'].ljust(max_len_group + 4)
        exch  = row['exchange_variable'].ljust(max_len_exch + 1)
        glob  = row['global_variable_fmt'].ljust(max_len_global + 1)
        desc  = row['description']
        return f"{group}{exch}:= {glob}//{desc}"

    righe = df.apply(formatta_riga, axis=1)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(righe))

    print(f"[OK] File generato: {output_path}")
    messagebox.showinfo("Successo", f"File generato:\n{output_path}")

# --- MAIN ---
if __name__ == "__main__":
    path_db = scegli_file()
    if not path_db:
        print("Nessun file selezionato.")
    elif not os.path.exists(path_db):
        print("File non trovato.")
    else:
        tabella = "mach_sts_bool"
        file_output = os.path.splitext(os.path.basename(path_db))[0] + "_export.txt"
        genera_file_txt(path_db, tabella, file_output)
