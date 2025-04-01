from fb_choose_file import scegli_file
from fb_generate_file import genera_file_txt
from constants import PLC,HMI
import os

# --- MAIN ---
if __name__ == "__main__":
    path_db = scegli_file()
    if not path_db:
        print("Nessun file selezionato.")
    elif not os.path.exists(path_db):
        print("File non trovato.")
    else:
        # Lista di tuple: (nome_tabella, intestazione blocco)
        sts_tables = [
            ("mach_sts_bool", "STS BOOL"),
            ("mach_sts_int", "STS INT"),
            ("mach_sts_dint", "STS DINT"),
        ]

        par_tables = [
            ("par_bool", "PAR BOOL"),
            ("par_int", "PAR INT"),
        ]
        genera_file_txt(path_db, sts_tables=sts_tables, par_tables=par_tables, device=PLC, path_db=path_db)
        genera_file_txt(path_db, sts_tables=sts_tables, par_tables=par_tables, device=HMI, path_db=path_db)
