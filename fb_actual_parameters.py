from constants import pers_vars_bool, pers_vars_int, PLC, HMI, netvar_par_bool, netvar_par_int



def actual_par_block(df, header_title, device):
    # Formatta i campi di base
    df["group_fmt"] = df["group"].apply(lambda g: f"(*{g}*)")
    max_len_group = df["group_fmt"].str.len().max()

    # Description
    df["description"] = df["description"].fillna("")
    
    # Support var
    if device == PLC:
        if header_title == "PAR BOOL":
            df["par_support_var"] = df["n"].apply(lambda n: f"{pers_vars_bool}[{n}]")
        else:
            df["par_support_var"] = df["n"].apply(lambda n: f"{pers_vars_int}[{n}]")
    else:
        if header_title == "PAR BOOL":
            df["par_support_var"] = df["n"].apply(lambda n: f"{netvar_par_bool}[{n}]")
        else:
            df["par_support_var"] = df["n"].apply(lambda n: f"{netvar_par_int}[{n}]")
    max_len_supp_var = df["par_support_var"].str.len().max()

    # Global variable name
    max_len_glob = df["global_variable"].str.len().max()                    # Calcolo lunghezza cella per tabulare
    df["padding_glob"] = df["global_variable"].apply(lambda g: " " * (max_len_glob - len(g)))
    
    # Measurment unit
    if "measurment_unit" in df.columns:
        df["measurment_unit_fmt"] = df["measurment_unit"].fillna("-").apply(lambda u: f"[{u}]")      # Prepara le colonne formattate
    else:
        df["measurment_unit_fmt"] = ""  # oppure df["unit_fmt"] = [""] * len(df)                    # Oppure se non esiste la colonna, lascio vuoto
    max_len_unit = df["measurment_unit_fmt"].str.len().max()  

    # Intestazione del blocco
    intestazione = [
        "",
        "/" * 60,
        f"// ACTUAL {header_title}",
        "/" * 60,
        ""
    ]

    # Format singola riga
    def formatta_riga(row):
        group       = row["group_fmt"].ljust(max_len_group)
        glob        = row["global_variable"]
        support_var = row["par_support_var"].ljust(max_len_supp_var)
        glob_spaces = row['padding_glob']
        unit        = row['measurment_unit_fmt'].ljust(max_len_unit)
        desc        = row["description"]

        """if device == PLC:
            return f"{group} {glob_spaces}{glob} := {support_var}; //{unit} {desc}"
        else:"""
        return f"{group} {glob_spaces}{glob} := {support_var}; //{unit} {desc}"

    righe = df.apply(formatta_riga, axis=1).tolist()
    return intestazione + righe
