def format_data(data_obj=None):
    if data_obj:
        data_formatada = data_obj.strftime("%d-%m-%Y")
        return data_formatada
    return None

def format_telefone(telefone=None):
    if telefone:
        telefone = telefone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        return telefone
    return None

def format_telPmascara(telefone):
    telefone = str(telefone)  # 79914641125
    return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"

