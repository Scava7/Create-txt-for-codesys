import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox
from fb_generate_block import sts_blocks
from fb_default_parameters import default_parameters_block
from constants import PLC,HMI
import os

def genera_file_txt(db_path, sts_tables, par_tables, device, path_db):
    conn = sqlite3.connect(db_path)
    contenuto = []

    # write the status block on both file (PLC and HMI)
    for nome_tabella, header_label in sts_tables:
        df = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
        blocco_status = sts_blocks(df, header_label, device)
        contenuto.extend(blocco_status)

    # write the default parameters block only on PLC file
    if device == PLC:
        for nome_tabella, header_label in par_tables:
            df_par_bool = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
            blocco_default_par_bool = default_parameters_block(df_par_bool, header_label)
            contenuto.extend(blocco_default_par_bool)

    conn.close()

    output_path = os.path.splitext(os.path.basename(path_db))[0] + f"_{device}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contenuto))

    print(f"[OK] File generato: {output_path}")
    messagebox.showinfo("Successo", f"File generato:\n{output_path}")