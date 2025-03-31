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
        filetypes=[("Database SQLite", "*.db *.sqlite3"),("Database SQLite", "*.db *.sqlite") , ("Tutti i file", "*.*")]
    )

def prepara_blocco(df, header_title):
    # Prepara le colonne formattate
    df["group_fmt"] = df["group"].apply(lambda g: f"(*{g}*)")
    df["global_variable_fmt"] = df["global_variable"].apply(lambda g: f"{g};")
    df["description"] = df["description"].fillna("")

    # Calcolo larghezze massime
    max_len_group = df["group_fmt"].str.len().max()
    max_len_exch = df["exchange_variable"].str.len().max()
    max_len_glob = df["global_variable_fmt"].str.len().max()

    # Intestazione del blocco
    intestazione = [
        "",
        "/" * 60,
        f"// {header_title}",
        "/" * 60,
        ""
    ]

    # Formattazione righe
    def formatta_riga(row):
        group = row['group_fmt'].ljust(max_len_group + 4)
        exch = row['exchange_variable'].ljust(max_len_exch + 4)
        glob = row['global_variable_fmt'].ljust(max_len_glob + 4)
        desc = row['description']
        return f"{group}{exch}:= {glob}//{desc}"

    righe = df.apply(formatta_riga, axis=1).tolist()

    return intestazione + righe

def genera_file_txt(db_path, tabelle, output_path):
    conn = sqlite3.connect(db_path)
    contenuto = []

    for nome_tabella, header_label in tabelle:
        df = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
        blocco = prepara_blocco(df, header_label)
        contenuto.extend(blocco)

    conn.close()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contenuto))

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
        # Lista di tuple: (nome_tabella, intestazione blocco)
        tabelle_da_esportare = [
            ("mach_sts_bool", "STS BOOL"),
            ("mach_sts_int", "STS INT"),
        ]
        file_output = os.path.splitext(os.path.basename(path_db))[0] + "_export.txt"
        genera_file_txt(path_db, tabelle_da_esportare, file_output)
