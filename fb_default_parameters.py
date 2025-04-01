
def default_parameters_block(df, header_title):
    # Prepara colonne formattate
    df["group_fmt"] = df["group"].apply(lambda g: f"(*{g}*)")
    df["description"] = df["description"].fillna("")

    if header_title == "PAR BOOL":
        df["factory_value_fmt"] = df["factory_value"].apply(lambda val: "TRUE" if str(val).strip() in ("1", "True", "true") else "FALSE")
    else:
        df["factory_value_fmt"] = df["factory_value"].fillna("").astype(str)

    # Measurment unit
    if "measurment_unit" in df.columns:
        df["measurment_unit_fmt"] = df["measurment_unit"].fillna("-").apply(lambda u: f"[{u}]")      # Prepara le colonne formattate
    else:
        df["measurment_unit_fmt"] = ""  # oppure df["unit_fmt"] = [""] * len(df)                    # Oppure se non esiste la colonna, lascio vuoto
    


    # Calcolo larghezze per padding
    max_len_group = df["group_fmt"].str.len().max()
    max_len_exch = df["exchange_variable"].str.len().max()
    max_len_val = df["factory_value_fmt"].str.len().max()
    max_len_unit = df["measurment_unit_fmt"].str.len().max()  

    # Intestazione del blocco
    intestazione = [
        "",
        "/" * 60,
        f"// DEFAULT {header_title}",
        "/" * 60,
        ""
    ]

    # Formattazione righe
    def formatta_riga(row):
        group   = row["group_fmt"].ljust(max_len_group)
        exch    = row["exchange_variable"].ljust(max_len_exch)
        value   = row["factory_value_fmt"].ljust(max_len_val)
        unit    = row['measurment_unit_fmt'].ljust(max_len_unit)
        desc    = row["description"]
        return f"{group} {exch} := {value}; //{unit} {desc}"

    righe = df.apply(formatta_riga, axis=1).tolist()
    return intestazione + righe
