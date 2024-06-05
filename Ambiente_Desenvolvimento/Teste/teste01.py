import json

processos = [1,2,3,4,5,6,7,8,9]

# Dados a serem convertidos em JSON
fromJSON = []
for processo in processos:
    dados = {
        "NumeroProcesso": f"{processo}"
    }
    fromJSON.append(dados)

# Convertendo dados em JSON
json_string = json.dumps(fromJSON ,indent=4)  # indent=4 para uma formatação mais legível

# Escrevendo JSON em um arquivo
with open("dados.json", "w") as arquivo:
    arquivo.write(json_string)
