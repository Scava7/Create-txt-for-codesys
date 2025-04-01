
def default_parameters_block(df, header_title):
    # Prepara colonne formattate
    df["group_fmt"] = df["group"].apply(lambda g: f"(*{g}*)")
    df["description"] = df["description"].fillna("")
    if header_title == "PAR BOOL":
        df["factory_value_fmt"] = df["factory_value"].apply(lambda val: "TRUE" if str(val).strip() in ("1", "True", "true") else "FALSE")
    else:
        df["factory_value_fmt"] = df["factory_value"]

    # Calcolo larghezze per padding
    max_len_group = df["group_fmt"].str.len().max()
    max_len_exch = df["exchange_variable"].str.len().max()
    max_len_val = df["factory_value_fmt"].str.len().max()

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
        group = row["group_fmt"].ljust(max_len_group)
        exch = row["exchange_variable"].ljust(max_len_exch)
        value = row["factory_value_fmt"].ljust(max_len_val)
        desc = row["description"]
        return f"{group} {exch} := {value}; // {desc}"

    righe = df.apply(formatta_riga, axis=1).tolist()
    return intestazione + righe
