def formataProcessoCNJNovo(processo_parametro):
    processo = processo_parametro[1:21]
    num_processo = f"{processo[:7]}"
    digito = f"{processo[7:9]}"
    ano = f"{processo[9:13]}"
    j = "8"
    tr= "26"
    comarca = f"{processo[16:]}"
    
    processo_formatado = (f"{num_processo}-{digito}.{ano}.{j}.{tr}.{comarca}")
    
    return processo_formatado

def formataProcessoCNJAntigo(processo_parametro):
    processo = processo_parametro[:15]
    comarca = f"0{processo[:3]}"
    ano = f"{processo[5:9]}"
    num_processo = f"0{processo[9:]}"
    j = "8"
    tr = "26"
    digito = "00"
    
    processo_formatado_INT = f"{num_processo}{ano}{j}{tr}{comarca}{digito}"
    processo_formatado_INT = int(processo_formatado_INT)
    digito = 98 - (processo_formatado_INT % 97)

    processo_formatado = f"{num_processo}-{digito}.{ano}.{j}.{tr}.{comarca}"
    
    return processo_formatado

def formataProcessoDigitadoFormatado(processo_parametro):
    
    return processo_parametro

def formataProcessoDigitadoCorrido(processo_parametro):
    processo = processo_parametro[:7]
    digito = processo_parametro[7:9]
    ano = processo_parametro[9:13]
    j = processo_parametro[13:14]
    tr = processo_parametro[14:16]
    comarca = processo_parametro[16:20]

    processo_formatado = f"{processo}-{digito}.{ano}.{j}.{tr}.{comarca}"
    return processo_formatado