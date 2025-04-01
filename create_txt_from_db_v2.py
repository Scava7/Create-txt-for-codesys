import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

PLC = "PLC"
HMI = "HMI"

def scegli_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Scegli un database SQLite",
        filetypes=[("Database SQLite", "*.db *.sqlite3"),("Database SQLite", "*.db *.sqlite") , ("Tutti i file", "*.*")]
    )

def sts_blocks(df, header_title, device):
    
    # Group
    df["group_fmt"] = df["group"].apply(lambda g: f"(*{g}*)")   # Prepara le colonne formattate
    max_len_group = df["group_fmt"].str.len().max()             # Calcolo lunghezza cella per tabulare
    
    # Exchange variable name
    max_len_exch = df["exchange_variable"].str.len().max()    # Calcolo lunghezza cella per tabulare

    # Global variable name
    max_len_glob = df["global_variable"].str.len().max()                    # Calcolo lunghezza cella per tabulare

    # Spazi di compensazione per global_variable
    df["padding_glob"] = df["global_variable"].apply(lambda g: " " * (max_len_glob - len(g)))
    
    # Measurment unit
    if "measurment_unit" in df.columns:
        df["measurment_unit_fmt"] = df["measurment_unit"].fillna("-").apply(lambda u: f"[{u}]")      # Prepara le colonne formattate
    else:
        df["measurment_unit_fmt"] = ""  # oppure df["unit_fmt"] = [""] * len(df)                    # Oppure se non esiste la colonna, lascio vuoto
    max_len_unit = df["measurment_unit_fmt"].str.len().max()                                        # Calcolo lunghezza cella per tabulare

    # Description
    df["description"] = df["description"].fillna("")    #riempi celle vuote con ""

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
        group       = row['group_fmt'].ljust(max_len_group)
        exch        = row['exchange_variable'].ljust(max_len_exch)
        glob        = row['global_variable']
        glob_spaces = row['padding_glob']
        unit        = row['measurment_unit_fmt'].ljust(max_len_unit)
        desc        = row['description']

        if device == PLC:
            return f"{group} {exch} := {glob};{glob_spaces} //{unit} {desc}"
        else:
            return f"{group} {glob_spaces}{glob} := {exch}; //{unit} {desc}"

    righe = df.apply(formatta_riga, axis=1).tolist()

    return intestazione + righe

def genera_file_txt(db_path, tabelle, device):
    conn = sqlite3.connect(db_path)
    contenuto = []

    for nome_tabella, header_label in tabelle:
        df = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
        blocco = sts_blocks(df, header_label, device)
        contenuto.extend(blocco)

    conn.close()

    output_path = os.path.splitext(os.path.basename(path_db))[0] + f"_{device}.txt"

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
            ("mach_sts_dint", "STS DINT"),
        ]
        genera_file_txt(path_db, tabelle_da_esportare, device=PLC)
        genera_file_txt(path_db, tabelle_da_esportare, device=HMI)
