# Função para converter listas para string formatada
def getArrayString(list_: list, space_heranca="") -> str:
    if len(list_) == 0:
        return "[]"

    string = "[\n"
    space = space_heranca + "   "

    for elemento in list_:
        string += space
        # Verificar tipo de dado do elemento
        if isinstance(elemento, list):
            string += getArrayString(elemento, space)
        elif isinstance(elemento, dict):
            string += getDictString(elemento, space)
        else:
            string += f"'{elemento}'"
        string += ",\n"

    string += space_heranca + "]"
    return string  # Aqui estava faltando o return

# Função para converter dict para string formatada
def getDictString(dict_: dict, space_heranca="") -> str:
    string = "{\n"
    space = space_heranca + "   "

    for key, value in dict_.items():
        # Criar primeira linha do dicionário
        string += space + f"{key} : "
        # Verificar o tipo de dado do valor
        if isinstance(value, list):
            string += getArrayString(value, space)
        elif isinstance(value, dict):
            string += getDictString(value, space)
        else:
            string += f"'{value}'"
        string += "\n"

    string += space_heranca + "}"
    return string


