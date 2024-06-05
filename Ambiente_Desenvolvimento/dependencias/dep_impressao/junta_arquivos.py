from PyPDF2 import PdfReader, PdfWriter

def juntar_pdf(arquivo1, arquivo2, arquivo3, arquivo4, arquivo5, arquivo6, arquivo7, arquivo8, arquivo9, arquivo_saida):
    # Abrir os arquivos PDF
    pdf1 = PdfReader(open(arquivo1, "rb"))
    pdf2 = PdfReader(open(arquivo2, "rb"))
    pdf3 = PdfReader(open(arquivo3, "rb"))
    pdf4 = PdfReader(open(arquivo4, "rb"))
    pdf5 = PdfReader(open(arquivo5, "rb"))
    pdf6 = PdfReader(open(arquivo6, "rb"))
    pdf7 = PdfReader(open(arquivo7, "rb"))
    pdf8 = PdfReader(open(arquivo8, "rb"))
    pdf9 = PdfReader(open(arquivo9, "rb"))

    # Criar o arquivo de saída
    output = PdfWriter()

    # Adicionar todas as páginas do primeiro arquivo
    for page in pdf1.pages:
        output.add_page(page)

    # Adicionar todas as páginas do segundo arquivo
    for page in pdf2.pages:
        output.add_page(page)
        
        # Adicionar todas as páginas do segundo arquivo
    for page in pdf3.pages:
        output.add_page(page)
        
    for page in pdf4.pages:
        output.add_page(page)
    
    for page in pdf5.pages:
        output.add_page(page)
    
    for page in pdf6.pages:
        output.add_page(page)
    
    for page in pdf7.pages:
        output.add_page(page)
    
    for page in pdf8.pages:
        output.add_page(page)
    
    for page in pdf9.pages:
        output.add_page(page)
    

    # Salvar o arquivo de saída
    with open(arquivo_saida, "wb") as out_file:
        output.write(out_file)

# Teste
juntar_pdf("1.pdf", "2.pdf", "3.pdf", "4.pdf", "5.pdf", "6.pdf", "7.pdf", "8.pdf", "9.pdf", "arquivo_saida.pdf")



