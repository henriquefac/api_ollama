import re

def filtrar(text: str):
    # Lista de elementos que deseja remover do texto
    lista_de_elementos = ["\r"]
    
    # Remove os elementos indesejados usando a função recombine
    text = recombine(text, lista_de_elementos)
    
    # Divide o texto em linhas de acordo com '\n'
    lines = text.split("\n")
    
    # Remove linhas vazias
    lines = [line for line in lines if line.strip()]
    
    result: list = []

    for line in lines:
            # Verifica se a linha contém principalmente letras (mais de 50% letras)
            line = line.strip()  # Remove espaços em branco no início e fim da linha
            if len(re.findall(r'[a-zA-Z]', line)) > len(line) / 2:
                result.append(line)
    
    return ("\n").join(result)

def recombine(text: str, lista: list[str]):
    # Remove cada elemento indesejado da lista
    for element in lista:
        text = text.replace(element, "")
    return text




if __name__ == "__main__":
    # Teste com exemplo
    texto_exemplo = "Linha 1\r\nLinha 2\n\n\rLinha 3"
    filter(texto_exemplo)
