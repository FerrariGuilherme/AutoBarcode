import dependencias.formata_processos as formata_processos
import flet as ft
import pickle
from flet_route import Params,Basket 
from time import sleep
from dependencias.database import bd
from random import randint
from dependencias.dep_impressao.impressao import criar_pdf
from dependencias.apotamento_ambiente import aponta_pdf
from win32 import win32api
from win32 import win32print
from datetime import date




class SaidaView:
    def __init__(self):
        ...

    def view(self,page:ft.page,params:Params,basket:Basket):
        
        ##
        #VARIAVEIS
        ##
        
        global listagem_processos
        listagem_processos = []
        
        global processos_unico
        processos_unico = []
        
        ##
        #FUNCOES
        ##
        
        #Carrega arquivo de log - login_data.pkl
        with open("login_data.pkl", "rb") as file:
            usuario = pickle.load(file)
        
        #Navega para tela HOME
        def irParaTelaHome(e):
            listagem_processos=[]
            processos_unico=[]
            listView.controls=[]
            page.go('/home')
        
        #Caixa de dialogo simples
        def caixaDeDialogoSimples(titulo, texto = None, content = None):
            try:
                page.dialog.open=False
                page.update()
            except:
                pass
            if texto != None:
                page.dialog = ft.AlertDialog(title=ft.Text(value=f"{titulo}", size=18, weight=ft.FontWeight.BOLD),content=ft.Text(f"{texto}"), open=True)
            
            else:
                page.dialog = ft.AlertDialog(title=ft.Text(value=f"{titulo}", size=18, weight=ft.FontWeight.BOLD),content=content, open=True,)
                
            page.update()
            
        #Exclui processo da ListView
        def excluiProcessoDaListView(e):
            remover = []
            for item in listView.controls:
                if item.value == True:
                    
                    remover.append(item)
            for item in remover:
                listagem_processos.pop(processos_unico.index(f"{item.label[:25]}"))
                processos_unico.remove(item.label[:25])
                listView.controls.remove(item)
            
            txt_processos.value=f"      PROCESSOS: {len(listView.controls)}"
            page.update()
        
        #Coleta os processos escaneados e adiciona na listView
        def adicionaScaneadoNaListView(e):
            #Diferenciamos o formato CNJ do processo por '+'
            #Se tiver '+' no processo escaneado é o novo formato
            #Se não tiver '+' é o CNJ antigo
            
            #Redefine a msg de erro do campo SCANNER
            txtfield_scanner.error_text=None
            
            #Novo formato CNJ
            if '+' in txtfield_scanner.value or '=' in txtfield_scanner.value:
                processo_formatado = formata_processos.formataProcessoCNJNovo(txtfield_scanner.value)            
            
            elif ".8.26." in txtfield_scanner.value:
                processo_formatado = formata_processos.formataProcessoDigitadoFormatado(txtfield_scanner.value)   
            #digitado corrido
            elif len(txtfield_scanner.value) == 20:
                processo_formatado = formata_processos.formataProcessoDigitadoCorrido(txtfield_scanner.value)
            #Antigo formato CNJ
            else:
                processo_formatado = formata_processos.formataProcessoCNJAntigo(txtfield_scanner.value)
            
            #Verifica se processo escaneado condiz com a comarca selecionada
            cod_comarca = bd.consultar_database(f"SELECT * FROM 'sistema.comarca' WHERE comarca_text = '{drop_comarca.value}'")
            if processo_formatado[21:] != cod_comarca[0][0]:
                
                ##NESTA ETAPA O CODIGO "IF" VERIFICA SE A COMARCA SELECIONADA É DA CAPITAL E SE OS PROCESSOS BIPADOS É 0100 OU 0583
                ##PARA VOLTAR AO CODIGO ORIGNAL - REMOVER LINHAS DO IF E PASS
                ##E A PARTE DO ELSE SERA DO ESCOPO "if processo_formatado[21:] != cod_comarca[0][0]:"
                if (cod_comarca[0][0] == "0014" and processo_formatado[21:] == "0100") or (cod_comarca[0][0] == "0014" and processo_formatado[21:] == "0100"):
                    pass
                else:
                    page.dialog = ft.AlertDialog(title=ft.Text(f"Este processo não pertence a comarca de ('{cod_comarca[0][1]}')"), on_dismiss=None, open=True)

                    txtfield_scanner.value=None
                    txtfield_scanner.error_text=" "
                    txtfield_scanner.error_style=ft.TextStyle(size=0)
                    txtfield_scanner.focus()
                    page.update()
                    return
             
            #Verifica se o processo já foi escaneado anteriormente se sim finaliza a função com return
            if processo_formatado in processos_unico:
                page.dialog = ft.AlertDialog(title=ft.Text("Processo já escaneado nesta remessa!"), on_dismiss=None, open=True)

                txtfield_scanner.value=None
                txtfield_scanner.error_text=" "
                txtfield_scanner.error_style=ft.TextStyle(size=0)
                txtfield_scanner.focus()
                page.update()
                return
            
            #Verifica se o processo esta com saida pendente (Se não tiver saida pendente significa que não tem cadastro do processo em aberto, só possivel realizar saida de um processo com em aberto)
            if len(bd.consultar_database(f"SELECT processo FROM 'processos.pendente_de_saida' WHERE processo = '{processo_formatado}'")) >= 1:
                pass
            else:
                caixaDeDialogoSimples(titulo="Alerta: Não localizado no sistema",texto="Esta ação não pode ser concluída no momento\n\nNão foi localizado nenhum registro de entrada em aberto.\nAntes de realizar a saída deste processo é necessario realizar a entrada.")
                txtfield_scanner.value=""
                txtfield_scanner.focus()
                return
            
            #Verifica se foi selecionada algum situação
            if drop_situacao.value == None:
                caixaDeDialogoSimples("Nenhuma situação selecionada", "Para registrar a saída deste processo é necessario selecionar alguma situação.")
                txtfield_scanner.value=None
                txtfield_scanner.focus()
                return
            else:
                processos_unico.append(processo_formatado)
            
            #Verifica se possui volume
            if txtfield_volume.value != "" :
                processo_completo = f"{processo_formatado}    --    {txtfield_volume.value} Vol"
            #Verifica se possui Apenso
            if txtfield_apenso.value != "" :
                processo_completo = f"{processo_formatado}    --    {txtfield_apenso.value} Ape"
            #Verifica se possui volume e apenso
            if txtfield_apenso.value != "" and txtfield_volume.value != "":
                processo_completo = f"{processo_formatado}    --    {txtfield_volume.value} Vol / {txtfield_apenso.value} Ape"
            #Verifica se não possui vol e ape
            if txtfield_apenso.value == "" and txtfield_volume.value == "":
                processo_completo = f"{processo_formatado}"
            #Adiciona o processo já formatado com vol e ape na listView
            listView.controls.append(ft.Checkbox(label=processo_completo))
            #Formata a variavel processo completo para uma array onde [0] é o numero do processo formatado [1] Volumes [2] Apensos [3] Providencia [4] Situacao
            processo_completo = [
                f"{processo_formatado}",
                f"{txtfield_volume.value}",
                f"{txtfield_apenso.value}",
                bd.consultar_database(f"SELECT * FROM 'processos.situacoes' WHERE situacao = '{drop_situacao.value}'")[0][1], 
                bd.consultar_database(f"SELECT * FROM 'processos.situacoes' WHERE situacao = '{drop_situacao.value}'")[0][2],]
            #processo_completo = [f"{processo_formatado}", f"{txtfield_volume.value}", f"{txtfield_apenso.value}", f"{bd.consultar_database("SELECT * FROM 'processos.situacoes' WHERE situacao = 'Débito Remitido'")[0][1]}", f"{bd.consultar_database("SELECT * FROM 'processos.situacoes' WHERE situacao = 'Débito Remitido'")[0][2]}' ]
            
            #Adiciona array com o numero do processo - Vol - Ape na array listagem de processos
            listagem_processos.append(processo_completo)
            #Deixa em branco os campos SCANNER VOL APE, e define o focus no scanner
            txtfield_scanner.value=None
            txtfield_volume.value=None
            txtfield_apenso.value=None
            txtfield_scanner.focus()
            #Altera a label que exibe a quantidade de processos escaneados
            txt_processos.value=f"      PROCESSOS: {len(listView.controls)}"
            #Atualiza a pagina
            page.update()
                
            txtfield_scanner.focus()

        #Abre a remessa e registra no Banco de Dados a remessa aberta        
        def abrir_remessa(e):
            #Coleta os valores de todos os campos
            comarca = bd.consultar_database(f"SELECT comarca FROM 'sistema.comarca' WHERE comarca_text = '{drop_comarca.value}'")
            #O valor da variavel comarca é o retorna da consulta no banco de dados para pegar somente o nome da comarca, e o retorno da consulta no banco de dados é uma array
            #No Try abaixo ocorre a tentativa de transformar a varivaer comarca de array para str, pode acontecer de o retorno da consulta no banco de dados ser vazio, caso o usiario não informar comarca
            #Se a array for vazia, não possivel, transforma de array para str
            try:
                comarca = comarca[0][0]
            except:
                comarca=None
            destino = drop_destino.value
            data = txtfield_data.value
            remessa = txtfield_remessa.value
            responsavel = usuario[0][1]
            #Altera a borda de todos os campos para verde
            drop_comarca.border_color=ft.colors.GREEN
            drop_destino.border_color=ft.colors.GREEN
            txtfield_data.border_color=ft.colors.GREEN
            #Define a mesagem de de erro de todos os campos para nulo
            drop_comarca.error_text=""
            drop_destino.error_text=""
            txtfield_data.error_text=""
            txtfield_remessa.error_text=""
            
            #Verifica se os campos estão preenchidos, se algum não estiver preenchido, altera a menssagem de erro
            if comarca == None:
                drop_comarca.error_text=" "
                drop_comarca.error_style=ft.TextStyle(size=0)
            if destino == None:
                drop_destino.error_text=" "
                drop_destino.error_style=ft.TextStyle(size=0)
            #Verifica se o campo de data esta preenchido corretamente
            if len(data) > 10 or len(data) < 10 or data[2:3] != "/" or data[5:6] != "/":
                txtfield_data.error_text=" "
                txtfield_data.error_style=ft.TextStyle(size=0)
                data=None
            #Verifica se a data informada é valida
            else:
                dia = data[:2]
                mes = data[3:5]
                ano = data[6:]
                try:
                    dia = int(dia)
                    mes = int(mes)
                    ano = int(ano)
                    if dia > 31 or dia < 0:
                        data=None
                        txtfield_data.error_text=" "
                        txtfield_data.error_style=ft.TextStyle(size=0)
                    if mes > 12 or mes < 0:
                        data=None
                        txtfield_data.error_text=" "
                        txtfield_data.error_style=ft.TextStyle(size=0)
                    if ano > 2025 or ano < 2023:
                        data=None
                        txtfield_data.error_text=" "
                        txtfield_data.error_style=ft.TextStyle(size=0)
                    
                    
                except:
                    data=None
                    txtfield_data.error_text=" "
                    txtfield_data.error_style=ft.TextStyle(size=0)
            if remessa == "":
                txtfield_remessa.error_text=" "
                txtfield_remessa.error_style=ft.TextStyle(size=0)
                remessa=None
                
            #Exibe a menssagem de erro "Remessa não criada" / e limpa a row de exibir msg de erro
            #Cada erro ao criar a remessa realiza um append da msg de erro na row, se não limpa a row, fica com muitas msgs de erro
            row_para_exibir_msg_de_erro_remessa.controls=[]
            row_para_exibir_msg_de_erro_remessa.controls.append(txt_remessa_nao_criada)
            
            #Verifica se remessa já existe
            if len(bd.consultar_database(f"SELECT * FROM 'processos.remessa' WHERE remessa = '{remessa}' and tipo = 'SAIDA' and comarca = '{comarca}'")) >= 1:
                row_para_exibir_msg_de_erro_remessa.controls=[]
                row_para_exibir_msg_de_erro_remessa.controls.append(txt_remessa_duplicada)
                txtfield_remessa.error_text=" "
                txtfield_remessa.error_style=ft.TextStyle(size=0)
                remessa=None

            #verifica se todos os campos não estão em branco
            if comarca != None and destino != None and data != None and remessa != None:
                #Limpa a row para remover msg de erro e realiza append a msg de sucesso
                row_para_exibir_msg_de_erro_remessa.controls=[]
                row_para_exibir_msg_de_erro_remessa.controls.append(txt_remessa_criada)
                
                #Registra a nova remessa no banco de dados
                bd.alterar_database(f"INSERT INTO 'processos.remessa' (remessa, tipo, comarca, responsavel, data) VALUES ('{remessa}', 'SAIDA', '{comarca}', '{responsavel}', '{data}')")
                
                #Desativa a primera parte
                drop_comarca.disabled=True
                drop_destino.disabled=True
                txtfield_data.read_only=True
                txtfield_remessa.read_only=True
                btn_Abrir_Remessa.disabled=True
                btn_voltar.disabled=True
                
                #Ativa a segunda parte
                txtfield_volume.disabled=False
                txtfield_apenso.disabled=False
                txtfield_scanner.disabled=False
                txtfield_scanner.focus()
                drop_situacao.disabled=False
                listView.disabled=False
                btn_Remover.disabled=False
                btn_SalvarRemessa.disabled=False
                
                #Limpa o arquivo cache de remessa atual
                with open("remessa_atual.pkl", "wb") as file:
                    pickle.dump("", file)
                    
            txtfield_scanner.focus()               
            page.update()
        
        #Salvar Remessa
        def salvarRemessa(e):
        
            def close_dlg(e):
                dlg_modal.open = False
                page.update()

            def registra_bd(e):
                close_dlg(e)
                caixaDeDialogoSimples(titulo="Salvando remessa", content=ft.ProgressBar(color="amber", bgcolor="#eeeeee"))
                
                
                #Adicionar os processo da remessa na tabela processo_remessa
                bd.alterar_database(f'UPDATE "processos.remessa" SET processos = "{listagem_processos}" WHERE remessa = "{txtfield_remessa.value}" AND tipo = "SAIDA"')
                txtfield_scanner.disabled=True
                #Adiciona os processos nas demais tabelas
                for processo in listagem_processos:
                    #Adiciona os processo da remessa na tabela processo.registro
                    bd.alterar_database(f"INSERT INTO 'processos.registro' (processo, registro, data, remessa, providencia, situacao, responsavel, observacao) VALUES ('{processo[0]}', 'SAIDA', '{txtfield_data.value}', '{txtfield_remessa.value}', '{processo[3]}', '{processo[4]}', '{usuario[0][1]}', '')")
                    #Remove o processo da tabela processos.pendentes de saida
                    bd.alterar_database(f"DELETE FROM 'processos.pendente_de_saida' WHERE processo = '{processo[0]}'")
                    #Varivael - texto que sera adicionado no historico do processo
                    historico = f"""____________________________________________________________

ID REGISTRO = $$   -   {processo[0]}

Tipo: SAIDA  -  {usuario[0][1]}

Prov: {processo[3]}
Sit: {processo[4]}

Data: {txtfield_data.value}
Resp: {usuario[0][1]}
Coma: {drop_comarca.value}
Reme: {txtfield_remessa.value}
Vol: {processo[1]}
Ape: {processo[2]}
Dest: {drop_destino.value}

"""
                    #Verifica se o processo já exite na tabela historico - Se não existir adiciona na tabela de historicos e depois adiciona o historico
                    if len(bd.consultar_database(f"SELECT processo FROM 'processos.historico' WHERE processo = '{processo[0]}'")) == 0:
                        bd.alterar_database(f"INSERT INTO 'processos.historico' (processo, historico) VALUES ('{processo[0]}', ' ')")     
                    #Adiciona a variavel historico na tabela de historico
                    bd.alterar_database(f"UPDATE 'processos.historico' SET historico = '{historico}' || historico WHERE processo = '{processo[0]}'")
                #Remove da tela a caixa de dialogo - "Realmente deseja salvar esta remessa ?"
                sleep(1)
                #Exibe caixa de dialogo simples informando que a remessa foi salva com sucesso
                caixaDeDialogoSimples(titulo="Ação concluida", texto="A remessa foi salva com sucesso.\nAgora realize a impressão do comprovante de remessa para prosseguir.")
                #Desativa os botoes REMOVER e SALVAR REMESSA
                btn_Remover.disabled=True
                btn_SalvarRemessa.disabled=True
                #Ativa o botao de impressão
                btn_Imprimir.disabled=False
                
                page.update()
  
            dlg_modal = ft.AlertDialog(
                title=ft.Text(value=f"Salvar remessa", size=18, weight=ft.FontWeight.BOLD),
                content=ft.Text(f"Realmente deseja salvar esta remessa ?"),
                actions=[ft.TextButton("Sim", on_click=registra_bd), ft.TextButton("Não", on_click=close_dlg)],
                open=True,
            )
            
            page.dialog = dlg_modal
            page.update()
        
        #Imprimir comprovante da remessa              
        def imprimir(e):

            comarca = bd.consultar_database(f"SELECT comarca FROM 'sistema.comarca' WHERE comarca_text = '{drop_comarca.value}'")[0][0]
            criar_pdf(nome_arquivo=f"{aponta_pdf}RS_{txtfield_remessa.value}_{comarca}.pdf", 
                      origem=f"PGE - {usuario[0][4]}", 
                      destino=f"{drop_destino.value}", 
                      comarca=f"{comarca}", 
                      remessa=f"{txtfield_remessa.value}", 
                      data_emissao=f"{txtfield_data.value}", 
                      total=f"{len(listagem_processos)}", 
                      expedido=f"{usuario[0][1]}",
                      processos=listagem_processos)
            
            btn_TelaInicial.disabled=False
            btn_Limpar.disabled=False
            
            filename = f"{aponta_pdf}RS_{txtfield_remessa.value}_{comarca}.pdf"
            printer_name = win32print.GetDefaultPrinter()

            win32api.ShellExecute(
                0,
                "printto",
                filename,
                '"' + printer_name + '"',
                ".",
                0
            )
            
            
            
            page.update()
        
        #Limpa tela
        def reset(e):
            listagem_processos.clear()
            processos_unico.clear()
            listView.controls.clear()
            
            drop_comarca.value=None
            drop_comarca.error_text=None
            drop_comarca.border_color=ft.colors.BLACK
            drop_comarca.disabled=False
            
            drop_destino.value=None
            drop_destino.error_text=None
            drop_destino.border_color=ft.colors.BLACK
            drop_destino.disabled=False
        
            txtfield_data.value=data_atual()
            txtfield_data.error_text=None
            txtfield_data.border_color=ft.colors.BLACK
            txtfield_data.read_only=False
            
            txtfield_remessa.value=f"{geraNumeroRemessa()}"
            txtfield_remessa.error_text=None
            txtfield_remessa.border_color=ft.colors.GREEN
            txtfield_remessa.read_only=True
            
            txtfield_apenso.value=None
            txtfield_apenso.error_text=None
            txtfield_apenso.border_color=ft.colors.BLACK
            txtfield_apenso.disabled=True
            
            txtfield_volume.value=None
            txtfield_volume.error_text=None
            txtfield_volume.border_color=ft.colors.BLACK
            txtfield_volume.disabled=True
            
            txtfield_scanner.value=None
            txtfield_scanner.error_text=None
            txtfield_scanner.border_color=ft.colors.BLACK
            txtfield_scanner.disabled=True
            
            txt_processos.value="      PROCESSOS: 0"
            
            btn_voltar.disabled=False
            btn_Abrir_Remessa.disabled=False
            
            drop_situacao.disabled=True
            drop_situacao.value=None
            btn_Remover.disabled=True
            btn_SalvarRemessa.disabled=True
            btn_Imprimir.disabled=True
            btn_TelaInicial.disabled=True
            btn_Limpar.disabled=True
            
            row_para_exibir_msg_de_erro_remessa.controls=[]
            
            
            
            page.update()
        
        #Gera o numero da remessa
        def geraNumeroRemessa():
            while True:
                remessa = randint(0000000, 9999999)
                if len(bd.consultar_database(f"SELECT remessa FROM 'processos.remessa' WHERE tipo = 'SAIDA' and remessa = '{remessa}'")) != 0:
                    pass
                else:
                    return remessa
                    break
        
        #Coleta data atual formato DD/MM/AAAA
        def data_atual():
            return date.today().strftime('%d/%m/%Y')
        
        
        ##
        #COMPONENTES
        ##
        
        drop_comarca = ft.Dropdown(width=430, border_width=0.8, border_color=ft.colors.BLACK)
        #Coleta as opcoes de comarca do banco de dados
        for item in bd.consultar_database("SELECT comarca_text FROM 'sistema.comarca'"):
            drop_comarca.options.append(ft.dropdown.Option(f"{item[0]}"))
        
        drop_destino = ft.Dropdown(width=430, height=55, text_size=15, border_width=0.8, border_color=ft.colors.BLACK)
        #Coleta as opcoes de destino do banco de dados
        for item in bd.consultar_database("SELECT destino FROM 'sistema.origem_destino' WHERE destino != 'DIGITALIZAÇÃO - (EMPRESA)' and destino != 'DIGITALIZAÇÃO - (INTERNO)'"):
            if item[0] == None:
                break
            drop_destino.options.append(ft.dropdown.Option(f"{item[0]}"))
            
        drop_situacao = ft.Dropdown(width=300, height=35, text_size=15, border_width=0.8, border_color=ft.colors.BLACK, content_padding=ft.padding.symmetric(horizontal=10), disabled=True)
        for item in bd.consultar_database("SELECT situacao FROM 'processos.situacoes'"):
            if item[0] == None:
                break
            drop_situacao.options.append(ft.dropdown.Option(f"{item[0]}"))
        
        txtfield_data = ft.TextField(label="Data de Saída", width=186, prefix_icon=ft.icons.CALENDAR_MONTH_OUTLINED, hint_text="DD/MM/AAAA", prefix_text="  ", height=50, border_width=0.8, border_color=ft.colors.BLACK, value=data_atual())
        
        txtfield_remessa = ft.TextField(width=186, hint_text="Remessa de Entrada", height=50, border_width=0.8, border_color=ft.colors.GREEN, read_only=True, value=f"{geraNumeroRemessa()}", prefix_text="RS - ")
        
        txt_remessa_criada = ft.Text(value="Remessa criada com sucesso !", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.GREEN)
        
        txt_remessa_duplicada = ft.Text(value="Esta remessa já existe!", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.RED)
        
        txt_remessa_nao_criada = ft.Text(value="Preencha todos os campos corretamente!", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.RED)
        
        row_para_exibir_msg_de_erro_remessa = ft.Row(width=489, height=80, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[])
        
        btn_voltar = ft.FilledTonalButton(width=100, height=50, on_click=irParaTelaHome, text="Voltar")
        
        btn_Abrir_Remessa = ft.ElevatedButton(width=230, height=50, text="Abrir Remessa", on_click=abrir_remessa)
        
        txtfield_volume = ft.TextField(width=100, hint_text="Volumes", label="Volumes", height=45, disabled=True, border_width=0.8, border_color=ft.colors.BLACK, input_filter=ft.NumbersOnlyInputFilter())
        
        txtfield_apenso = ft.TextField(width=100, hint_text="Apensos", label="Apensos", height=45, disabled=True, border_width=0.8, border_color=ft.colors.BLACK, input_filter=ft.NumbersOnlyInputFilter())
        
        txtfield_scanner = ft.TextField(width=430, hint_text="xxxxxxx-xx.xxxx.x.xx.xxx", label="SCANNER", on_submit=adicionaScaneadoNaListView, height=45, disabled=True, border_width=0.8, border_color=ft.colors.BLACK, content_padding=ft.padding.symmetric(horizontal=10))
        
        txt_processos = ft.Text(value=f"      PROCESSOS: 0", weight=ft.FontWeight.W_700, size=16, disabled=True)
        
        listView = ft.ListView(spacing=10, padding=5, height=350, width=475, divider_thickness=1, disabled=True, auto_scroll=True)
        
        btn_TelaInicial = ft.ElevatedButton(text="Tela Inicial", bgcolor=ft.colors.LIGHT_BLUE_300, color=ft.colors.WHITE, on_click=irParaTelaHome, disabled=True)
        
        btn_Remover = ft.ElevatedButton(text="Remover", bgcolor=ft.colors.RED_400, color=ft.colors.WHITE, disabled=True, on_click=excluiProcessoDaListView)
        
        btn_Imprimir = ft.ElevatedButton(text="Imprimir", bgcolor=ft.colors.BLUE_GREY_300, color=ft.colors.WHITE, disabled=True, on_click=imprimir)
        
        btn_SalvarRemessa = ft.ElevatedButton(text="Salvar Remessa", bgcolor=ft.colors.GREEN_400, color=ft.colors.WHITE, disabled=True, on_click=salvarRemessa)
        
        btn_Limpar = ft.ElevatedButton("Limpar", bgcolor=ft.colors.LIGHT_BLUE_300, color=ft.colors.WHITE, disabled=True, on_click=reset)
        
        width_main = page.window_width
        height_main = page.window_height

        return ft.View(
            route= "/registroSaida",
            bgcolor=ft.colors.WHITE,
            padding=0,
            controls=[
                ft.Column(
                    width=page.window_width,
                    height=page.window_height,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        #LINHA -- TITLE ENTRADA
                        ft.Row(
                            width=page.window_width,
                            height=30,
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value="Saída", weight=ft.FontWeight.BOLD)
                            ]
                            ),
                        #DIVISORIA
                        ft.Divider(height=1),
                        #LINHA QUE PEGA O RESTANTE DA TELA
                        ft.Row(
                            width=page.window_width,
                            height=page.window_height - 20,
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            controls=[
                                #COLUNA PARTE I
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    width=489,
                                    spacing=0,
                                    controls=[
                                        #ROW COMARCA
                                        ft.Row(
                                            width=489,
                                            height=150,
                                            controls=[
                                                #COLUNA DENTRO DA ROW PARA ALINHAR OS ITENS UM ABAIXO DO OUTRO
                                                ft.Column(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    width=489,
                                                    height=150,
                                                    controls=[
                                                        ft.Text(value="Comarca", weight=ft.FontWeight.W_500, size=20),
                                                        drop_comarca
                                                    ]
                                                ),
                                            ],
                                        ),
                                        #ROW destino
                                        ft.Row(
                                            width=489,
                                            height=150,
                                            controls=[
                                                #COLUNA DENTRO DA ROW PARA ALINHAR OS ITENS UM ABAIXO DO OUTRO
                                                ft.Column(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    width=489,
                                                    controls=[
                                                        ft.Text(value="Destino", weight=ft.FontWeight.W_500, size=20),
                                                        drop_destino
                                                    ]
                                                ),
                                            ],
                                        ),
                                        #ROW DATA // REMESSA
                                        ft.Row(
                                            width=489,
                                            height=130,
                                            controls=[
                                                #COLUNA DENTRO DA ROW PARA ALINHAR OS ITENS UM ABAIXO DO OUTRO
                                                ft.Column(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    width=244.5,
                                                    controls=[
                                                        ft.Text(value="Data", weight=ft.FontWeight.W_500, size=16),
                                                        txtfield_data
                                                    ]
                                                ),
                                                ft.Column(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    width=244.5,
                                                    controls=[
                                                        ft.Text(value="Remessa", weight=ft.FontWeight.W_500, size=16),
                                                        txtfield_remessa
                                                    ]
                                                ),
                                            ],
                                        ),
                                        #MSG SUCESSO - REMESSA CRIADA COM SUCESSO!
                                        row_para_exibir_msg_de_erro_remessa,
                                        #ROW BOTAO
                                        ft.Row(
                                            width=489,
                                            height=100,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                btn_voltar,
                                                btn_Abrir_Remessa
                                            ],
                                        ),
                                    ]
                                ),
                                #DIVISORIA
                                ft.VerticalDivider(width=1),
                                #COLUNA PARTE II
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=0,
                                    width=489,
                                    controls=[
                                        #ROW VOL / APE
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            width=300,
                                            height=75,
                                            controls=[
                                                ft.Column(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                                    width=150,
                                                    controls=[
                                                        txtfield_volume
                                                    ]
                                                ),
                                                ft.Column(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                                    width=150,
                                                    controls=[
                                                        txtfield_apenso
                                                    ]
                                                )
                                            ]
                                        ),
                                        #SCANNER
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            width=450,
                                            height=65,
                                            controls=[
                                                ft.Text(value="Situação", weight=ft.FontWeight.W_500, size=16),
                                                drop_situacao
                                            ]
                                        ),
                                        #ROW MENU SUSPENDO
                                        ft.Row(
                                            width=430,
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            height=65,
                                            controls=[
                                                txtfield_scanner
                                            ]
                                        ),
                                        #PROCESSOS
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.START,
                                            controls=[
                                                txt_processos
                                            ]
                                        ),
                                        # ROW CONTAINER - LIST_VIEW
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.START,
                                            height=300,
                                            controls=[
                                                ft.Container(
                                                    width=475,
                                                    height=270,
                                                    padding=0,
                                                    alignment=ft.alignment.top_left,
                                                    border=ft.border.all(1),
                                                    border_radius=ft.border_radius.all(10),
                                                    content=listView
                                                )
                                            ]
                                        ),
                                        #BOTOES PT I
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            height=40,
                                            controls=[
                                                btn_Remover,
                                                btn_SalvarRemessa,
                                                btn_Imprimir
                                            ]
                                        ),
                                        #BOTOES PT II
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            height=40,
                                            controls=[
                                                btn_TelaInicial,
                                                btn_Limpar
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ]
                )          
            ]
        )
        
       
       
