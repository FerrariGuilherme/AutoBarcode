from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from dependencias.dep_impressao.impressao_primeira_folha import criar_pdf_primeira_folha
from dependencias.dep_impressao.impressao_folha_meio import criar_pdf_folha_meio
from dependencias.dep_impressao.impressao_ultima_folha import criar_pdf_ultima_folha
from PyPDF2 import PdfReader, PdfWriter
import os

def pagina_unica(nome_arquivo, origem, destino, comarca, remessa, data_emissao, total, expedido, processos):
    
    processos_tratados = []
    indice = 0
    for p in processos:
        indice = indice + 1
        if indice < 10:
            indice = f"0{indice}"
            
        if p[1] != "" and p[2] != "":
            p = f"{indice}.)  {p[0]}  - {p[1]} Vol - {p[2]} Ape"
            processos_tratados.append(p)
        
        elif p[1] != "" and p[2] == "":
            p = f"{indice}.)  {p[0]}  - {p[1]} Vol"
            processos_tratados.append(p)

        elif p[2] != "" and p[1] == "":
            p = f"{indice}.)  {p[0]}  - {p[2]} Ape"
            processos_tratados.append(p)

        else:
            p = f"{indice}.)  {p[0]}"
            processos_tratados.append(p)
            
        indice = int(indice)
        
    processos = processos_tratados
    
    
    c = canvas.Canvas(f"{nome_arquivo}", pagesize=letter)
    largura, altura = letter
    
    # Logo e Título
    c.drawInlineImage("assets/logo.png", 1, altura - 100, width=250, height=55)  # Substitua "logo.jpg" pelo caminho da sua imagem de logotipo
    c.setFont("Helvetica-Bold", 12)
    c.drawString(220, altura - 70, "PROCURADORIA GERAL")
    c.drawString(220, altura - 85, "DO ESTADO DE SÃO PAULO")
    c.drawInlineImage("assets/logo2.png", 500, altura - 100, width=50, height=65)
    c.line(x1=20, x2=largura-20, y1=670, y2=670)
    c.line(x1=20, x2=largura-20, y1=585, y2=585)
    c.line(x1=20, x2=largura-20, y1=35, y2=35)
    c.drawInlineImage("assets/logo.png", x=(largura-130)/2, y=0, width=130, height=30)

    # Cabeçalhos da Tabela
    cabecalhos = ['Origem:', 'Destino:', 'Comarca:']
    cabecalhos2 = ['Remessa:', 'Data:', 'Total:']
    cabecalhos3 = ['Expedido por:', 'Recebido por:']
    
    x_inicial = 40
    y_inicial = altura - 150
    
    for cabecalho in cabecalhos:
        c.drawString(x_inicial, y_inicial, cabecalho)
        y_inicial -= 20
        
    x_inicial = 40
    y_inicial = altura - 150 
    
    for cabecalho in cabecalhos2:
        c.drawString(x_inicial+320, y_inicial, cabecalho)
        y_inicial -= 20
    
    x_inicial = 40
    y_inicial = altura - 720 
        
    for cabecalho in cabecalhos3:
        c.drawString(x_inicial, y_inicial, cabecalho)
        y_inicial -= 20

    # Outros Textos
    c.setFont("Helvetica", 10)
    textos = [
        (f'{origem}',), 
        (f'{destino}',), 
        (f'{comarca}',),

    ]
    
    textos2 = [
        (f'{remessa}',),
        (f'{data_emissao}',),
        (f'{total}',),
    ]
    
    textos3 = [
        (f'{expedido}',),
        ('Assinatura:  _______________________________________________      Data:   ____/____/______', '')
    ]

    y_inicial = altura - 150
    
    for texto in textos:
        x_texto_inicial = x_inicial + 65
        for item in texto:
            if item != '':
                c.drawString(x_texto_inicial, y_inicial, item)
                x_texto_inicial += 200
        y_inicial -= 20
        
    y_inicial = altura - 150
    
    for texto in textos2:
        x_texto_inicial = x_inicial + 385
        for item in texto:
            if item != '':
                c.drawString(x_texto_inicial, y_inicial, item)
                x_texto_inicial += 200
        y_inicial -= 20
        
    y_inicial = altura - 720
    
    for texto in textos3:
        x_texto_inicial = x_inicial + 95
        for item in texto:
            if item != '':
                c.drawString(x_texto_inicial, y_inicial, item)
                x_texto_inicial += 200
        y_inicial -= 20

    # Define o estilo da tabela
    style = TableStyle([
        ('LINEBELOW', (0,len(processos)), (-1,-1), 0.5, colors.grey),
    ])

    dados_tabela = []
    
    dados_tabela2 = []
    
    if len(processos) > 25:
        for item in processos:
            if len(dados_tabela) >= 25:
                dados_tabela2.append([item])
            else:
                dados_tabela.append([item])
        
        table2 = Table(dados_tabela2)
        table2.wrapOn(c, 400, 200)
        table2.drawOn(c, x_inicial+300, 550-((len(dados_tabela2)-1) * 18))
            
    else:
        for item in processos:
            dados_tabela.append([item])

    # Cria a tabela e define os dados
    if len(dados_tabela) <= 0:
        dados_tabela.append("Em branco")
    
    else:
        table = Table(dados_tabela)
        # Aplica o estilo à tabela
        table.setStyle(style)
        
        table.wrapOn(c, 400, 200)  # Define a largura e a altura disponíveis para a tabela
        table.drawOn(c, x_inicial, 550-((len(dados_tabela)-1) * 18))  # Define a posição onde a tabela será desenhada no canvas

    c.save()

def varias_paginas(nome_arquivo, origem, destino, comarca, remessa, data_emissao, total, expedido, processos):

    processos_tratados = []
    indice = 0
    for p in processos:
        indice = indice + 1
        if indice < 10:
            indice = f"0{indice}"
            
        if p[1] != "" and p[2] != "":
            p = f"{indice}.)  {p[0]}  - {p[1]} Vol - {p[2]} Ape"
            processos_tratados.append(p)
        
        elif p[1] != "" and p[2] == "":
            p = f"{indice}.)  {p[0]}  - {p[1]} Vol"
            processos_tratados.append(p)

        elif p[2] != "" and p[1] == "":
            p = f"{indice}.)  {p[0]}  - {p[2]} Ape"
            processos_tratados.append(p)

        else:
            p = f"{indice}.)  {p[0]}"
            processos_tratados.append(p)
            
        indice = int(indice)
        
    processos = processos_tratados
        
    
    
    caminho_pasta = 'dependencias/dep_impressao/impressao_temp/'
    arquivos = os.listdir(caminho_pasta)
    for arquivo in arquivos:
        os.remove(f"dependencias/dep_impressao/impressao_temp/{arquivo}")

    paginas = int(len(processos) / 50)+1

    pt = 0
    partes = {}   
    for processo in range(paginas):
        pt = pt+1
        partes[f"parte_{pt}"] = [processos[:50]]
        processos = processos[50:]
        
    pt = 0
    for folha in partes.values():
        pt = pt+1
        if pt == 1:
            criar_pdf_primeira_folha(nome_arquivo=f"{pt}.pdf", origem=origem, destino=destino, comarca=comarca, remessa=remessa, data_emissao=data_emissao, total=total, processos=folha[0])
        if pt == paginas:
            criar_pdf_ultima_folha(nome_arquivo=f"{pt}.pdf", remessa=remessa, expedido=expedido, pagina=f"{pt} / {paginas}", processos=folha[0])
        if pt > 1 and pt < paginas:
            criar_pdf_folha_meio(nome_arquivo=f"{pt}.pdf", remessa=remessa, pagina=f"{pt} / {paginas}", processos=folha[0])    

    pt = 0
    arquivo_final = PdfWriter()
    for paginas in range(paginas):
        pt = pt+1
        
        pagina = PdfReader(open(f"dependencias/dep_impressao/impressao_temp/{pt}.pdf", "rb"))
        
        for page in pagina.pages:
            arquivo_final.add_page(page)

    # Salvar o arquivo de saída
    with open(f"{nome_arquivo}", "wb") as out_file:
        arquivo_final.write(out_file)

def criar_pdf(nome_arquivo, origem, destino, comarca, remessa, data_emissao, total, expedido, processos):
    if len(processos) <= 50:
        pagina_unica(nome_arquivo=nome_arquivo, origem=origem, destino=destino, comarca=comarca, remessa=remessa, data_emissao=data_emissao, total=total, expedido=expedido, processos=processos)
        
    if len(processos) > 50:
        varias_paginas(nome_arquivo=nome_arquivo, origem=origem, destino=destino, comarca=comarca, remessa=remessa, data_emissao=data_emissao, total=total, expedido=expedido, processos=processos)
        



