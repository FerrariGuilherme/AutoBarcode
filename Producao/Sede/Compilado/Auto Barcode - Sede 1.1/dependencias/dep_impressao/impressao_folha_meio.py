from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors

def criar_pdf_folha_meio(nome_arquivo, remessa, pagina, processos):
    c = canvas.Canvas(f"dependencias/dep_impressao/impressao_temp/{nome_arquivo}", pagesize=letter)
    largura, altura = letter
    
    # Logo e Título
    c.drawInlineImage("assets/logo.png", 1, altura - 100, width=250, height=55)  # Substitua "logo.jpg" pelo caminho da sua imagem de logotipo
    c.setFont("Helvetica-Bold", 12)
    c.drawString(220, altura - 70, "PROCURADORIA GERAL")
    c.drawString(220, altura - 85, "DO ESTADO DE SÃO PAULO")
    c.drawInlineImage("assets/logo2.png", 500, altura - 100, width=50, height=65)
    c.line(x1=20, x2=largura-20, y1=670, y2=670)
    c.line(x1=20, x2=largura-20, y1=620, y2=620)
    c.drawString(x=270, y=40 , text="CONTINUA")
    c.line(x1=20, x2=largura-20, y1=35, y2=35)
    c.drawInlineImage("assets/logo.png", x=(largura-130)/2, y=0, width=130, height=30)

    # Cabeçalhos da Tabela
    cabecalhos = ['Remessa:']
    cabecalhos2 = [f'Pagina {pagina}']

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
        
    # Outros Textos
    c.setFont("Helvetica", 10)
    textos = [
        (f'{remessa}',), 
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

    y_inicial = altura - 720

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
