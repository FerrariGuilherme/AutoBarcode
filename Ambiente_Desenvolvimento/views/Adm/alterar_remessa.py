import flet as ft
import pickle
import cryptocode
import datetime
import locale
from flet_route import Params,Basket
from dependencias.database import bd
from dependencias.dep_impressao.impressao import criar_pdf
from dependencias.apotamento_ambiente import aponta_pdf
from win32 import win32api
from win32 import win32print

class AlterarRemessa:
    def __init__(self):
        ...

    def view(self,page:ft.page,params:Params,basket:Basket):
        
        ##
        #VARIAVEIS
        ##
        global processos_da_remessa
        processos_da_remessa = []
        global processos_da_remessa_backup
        processos_da_remessa_backup = []
        global alteracoes_remessa
        alteracoes_remessa = []
        
        with open("login_data.pkl", "rb") as file:
            usuario = pickle.load(file)
            
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        agora = datetime.datetime.now()
        data_hora_formatada = agora.strftime('%A, %d de %B de %Y %H:%M:%S')


        ##
        #FUNCOES
        ##
        
        #Carrega arquivo de log - login_data.pkl
        with open("login_data.pkl", "rb") as file:
            log = pickle.load(file)
        
        #Função para navegar entre as telas do menu de navegação
        def navChange(e):     
            if e == 0:
                navigation.on_change=page.go("/homeAdmProfile")
                
            if e == 1:
                navigation.on_change=page.go("/homeAdm")
            
            if e == 2:
                navigation.on_change=page.go("/")

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
        
        def close_dialog(e):
            alert_dialog.open = False
            page.update()
        
        def caixaDeDialogoComposta(titulo, texto=None, sim=None):

            global alert_dialog
            alert_dialog = ft.AlertDialog(
                    title=ft.Text(f"{titulo}"),
                    content=texto,
                    actions=[ft.TextButton("Sim", on_click=sim), ft.TextButton("Não", on_click=close_dialog)],
                    )
            #Exibe Dialogo
            page.dialog = alert_dialog
            alert_dialog.open = True
            page.update()
            
        def radiogroup_changed(e):
            processos_da_remessa.clear()
            processos_da_remessa_backup.clear()
            alteracoes_remessa.clear()
            lv_procesos_da_remessa.controls.clear()

            
            for processo in eval(bd.consultar_database(f"""SELECT * FROM 'processos.remessa' WHERE remessa = '{lv_resultadoBusca.controls[0].value.split("-")[1][1:]}' and tipo = '{lv_resultadoBusca.controls[0].value.split("-")[0].replace(" ", "")}'""")[0][3]):
                processos_da_remessa_backup.append([processo[0], processo[1], processo[2]])
                processo = ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.TextField(label=f"Processo",value=f"{processo[0]}", border="underline", width=175, text_size=12, text_style=ft.TextStyle(weight=ft.FontWeight.BOLD), content_padding=ft.padding.only(0,5,0,0)),
                        ft.TextField(label=f"Volumes",value=f"{processo[1]}", border="underline", read_only=True, width=50, text_size=12, label_style=ft.TextStyle(size=12)),
                        ft.TextField(label=f"Apensos",value=f"{processo[2]}", border="underline", read_only=True, width=50, text_size=12, label_style=ft.TextStyle(size=12)),
                    ]
                )
                
                processos_da_remessa.append(processo)
                    
            remessa = bd.consultar_database(f"""SELECT * FROM 'processos.remessa' WHERE remessa = '{lv_resultadoBusca.controls[0].value.split("-")[1][1:]}' and tipo = '{lv_resultadoBusca.controls[0].value.split("-")[0].replace(" ", "")}'""")[0]
            txtfield_Comarca.value = f"{remessa[4]}"
            txtfield_Responsavel.value = f"{remessa[5]}"
            txtfield_NumeroRemessa.value = f"{remessa[1]}"
            txtfield_Data.value = f"{remessa[6]}"
            txtfield_Total.value = f"{len(eval(remessa[3]))}"
            txtfield_Tipo.value = f"{remessa[2]}"
            
            
            

            page.update()
            
        def coletaProcessos(e):
            
            caixaDeDialogoSimples(titulo="Pesquisando remessa", content=ft.ProgressBar(color="amber", bgcolor="#eeeeee"))

            lista_de_remessas.controls.clear()
            
            remessas = bd.consultar_database(f"SELECT * FROM 'processos.remessa' WHERE remessa LIKE '%{txtfield_buscaRemessa.value}%'")
            for remessa in remessas:
                lista_de_remessas.controls.append(ft.Radio(value=f"{remessa[2]} - {remessa[1]}", label=f"{remessa[2]} - {remessa[1]}"))
            page.dialog.open=False
            txtfield_buscaRemessa.focus()
            page.update()
        
        #Imprimir comprovante da remessa 
        def imprimir(e):
            
            try:
                txtfield_Comarca.error_text=""
                txtfield_Responsavel.error_text=""
                txtfield_NumeroRemessa.error_text=""
                txtfield_Data.error_text=""
                txtfield_Total.error_text=""
                txtfield_Tipo.error_text=""
            
                match txtfield_Tipo.value:
                    case "ENTRADA":
                        tipo = "RE"
                    case "SAIDA":
                        tipo = "RS"
                    case "DIGITALIZACAO":
                        tipo = "RD"
                    
                
                filename = f"{aponta_pdf}{tipo}_{txtfield_NumeroRemessa.value}_{txtfield_Comarca.value}.pdf"
                printer_name = win32print.GetDefaultPrinter()

                win32api.ShellExecute(
                    0,
                    "printto",
                    filename,
                    '"' + printer_name + '"',
                    ".",
                    0
                )

            except:
                txtfield_Comarca.error_text=" "
                txtfield_Comarca.error_style=ft.TextStyle(size=0)
                
                txtfield_Responsavel.error_text=" "
                txtfield_Responsavel.error_style=ft.TextStyle(size=0)
                
                txtfield_NumeroRemessa.error_text=" "
                txtfield_NumeroRemessa.error_style=ft.TextStyle(size=0)
                
                txtfield_Data.error_text=" "
                txtfield_Data.error_style=ft.TextStyle(size=0)
                
                txtfield_Total.error_text=" "
                txtfield_Total.error_style=ft.TextStyle(size=0)
                
                txtfield_Tipo.error_text=" "
                txtfield_Tipo.error_style=ft.TextStyle(size=0)
                
            page.update()
        
        def salvarRemessa(e):
            alteracoes_remessa.clear()
            lv=ft.ListView(
                    spacing=10,
                    auto_scroll=False,
                    height=140,
                    width=465,
                    controls=[]
                )
            indice = 0
            
            # Verifica alterações na remessa
            for processo in processos_da_remessa:
                if processo.controls[0].value != processos_da_remessa_backup[indice][0] or processo.controls[1].value != processos_da_remessa_backup[indice][1] or processo.controls[2].value != processos_da_remessa_backup[indice][2]:
                
                    alteracoes_remessa.append([processo.controls[0].value, processo.controls[1].value, processo.controls[2].value])
                    lv.controls.append(ft.Text(value=f"{processos_da_remessa_backup[indice][0]} vol'{processos_da_remessa_backup[indice][1]}' - ape'{processos_da_remessa_backup[indice][2]}'  -->  {processo.controls[0].value} vol'{processo.controls[1].value}' - ape'{processo.controls[2].value}'", size=12, weight=ft.FontWeight.W_600))                    
                
                indice = indice+1

            if len(alteracoes_remessa) == 0:
                caixaDeDialogoSimples("Alterar Remessa", "Não há nenhuma alteração para salvar.")
                
            else:

                caixaDeDialogoComposta("Alterar Remessa", lv, alteraRemessabd)
                
        def alteraRemessabd(e):
            indice = 0
            close_dialog(e)
            for processo in processos_da_remessa: 
                
                bd.alterar_database(f"INSERT INTO 'processos.historico' (processo, historico) VALUES ('{processo.controls[0].value}', '')")
                bd.alterar_database(f"UPDATE 'processos.pendente_de_saida' SET processo = '{processo.controls[0].value}' WHERE processo = '{processos_da_remessa_backup[indice][0]}'")
                bd.alterar_database(f"UPDATE 'processos.registro' SET processo = '{processo.controls[0].value}' WHERE processo = '{processos_da_remessa_backup[indice][0]}'")
                bd.alterar_database(f"UPDATE 'processos.remessa' SET processos = REPLACE(processos, '{processos_da_remessa_backup[indice][0]}', '{processo.controls[0].value}') WHERE processos LIKE '%{processos_da_remessa_backup[indice][0]}%';")


                historico = f"""____________________________________________________________

ALTERAÇÃO DO PROCESSO POR:
Nome: {usuario[0][1]}

DE:     {processos_da_remessa_backup[indice][0]} 
PARA: {processo.controls[0].value}

Em {data_hora_formatada}

"""
   
                #Adiciona a variavel historico na tabela de historico
                bd.alterar_database(f"UPDATE 'processos.historico' SET historico = '{historico}' || historico WHERE processo = '{processo.controls[0].value}'")
                bd.alterar_database(f"UPDATE 'processos.historico' SET historico = '{historico}' || historico WHERE processo = '{processos_da_remessa_backup[indice][0]}'")
                

                indice = indice+1
                
            caixaDeDialogoSimples("Alteração de Remessa", "Remessa alterada com sucesso!")
            page.update()
        
        
        ##
        #COMPONENTES
        ##
        
        txtfield_buscaRemessa = ft.TextField(label="Remessa", prefix_icon=ft.icons.NUMBERS, width=200, on_submit=coletaProcessos)
        
        btn_busca = ft.OutlinedButton(content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Text(value="Buscar", size=14, weight=ft.FontWeight.W_600)]), height=40, width=120, on_click=coletaProcessos)
        
        lista_de_remessas = ft.Column(spacing=0,controls=[])
        
        global txtfield_Comarca
        txtfield_Comarca = ft.TextField(width=230, height=35, read_only=True, content_padding=ft.padding.symmetric(horizontal=10), text_size=14) 
        
        global txtfield_Responsavel
        txtfield_Responsavel = ft.TextField(width=230, height=35, read_only=True, content_padding=ft.padding.symmetric(horizontal=10), text_size=14)
        
        global txtfield_NumeroRemessa
        txtfield_NumeroRemessa = ft.TextField(width=230, height=35, read_only=True, content_padding=ft.padding.symmetric(horizontal=10), text_size=14)
        
        global txtfield_Data
        txtfield_Data = ft.TextField(width=230, height=35, read_only=True, content_padding=ft.padding.symmetric(horizontal=10), text_size=14)
        
        global txtfield_Total
        txtfield_Total = ft.TextField(width=170, height=35, read_only=True, content_padding=ft.padding.symmetric(horizontal=10), text_size=14)
        
        global txtfield_Tipo
        txtfield_Tipo = ft.TextField(width=170, height=35, read_only=True, content_padding=ft.padding.symmetric(horizontal=10), text_size=14)
        
        lv_resultadoBusca = ft.ListView(width=500, height=180, controls=[ft.RadioGroup(content=lista_de_remessas, on_change=radiogroup_changed)])
        
        lv_procesos_da_remessa = ft.ListView(width=750, height=300, padding=ft.padding.only(left=15, top=15, bottom=5), disabled=False, controls=processos_da_remessa)
        
        #Menu de navegação
        navigation = ft.NavigationRail(
                            selected_index=None,
                            label_type=ft.NavigationRailLabelType.ALL,
                            height=700,
                            scale=1.2,
                            width=110,
                            min_width=110,
                            min_extended_width=110,
                            group_alignment=-0.8,
                            leading=ft.Image(
                                    src="..\\assets\\12-removebg-preview-copia.png",
                                    height=220,
                                    width=70,
                                    fit=ft.ImageFit.CONTAIN,
                                    ),
                            bgcolor='#eeeeee',
                            destinations=[
                                ft.NavigationRailDestination(
                                    icon=ft.icons.PERSON_OUTLINE,
                                    selected_icon=ft.icons.PERSON, 
                                    label="Perfil",
                                    
                                ),
                                ft.NavigationRailDestination(
                                    icon=ft.icons.HOME_OUTLINED,
                                    selected_icon=ft.icons.HOME,
                                    label="Home",
                                ),
                                ft.NavigationRailDestination(
                                    icon=ft.icons.LOGOUT,
                                    selected_icon=ft.icons.LOGOUT,
                                    label_content=ft.Text("Sair"),
                                ),
                            ],
                            on_change=lambda e: navChange(e.control.selected_index),
                        )

        return ft.View(
            route="/alterarRemessa",
            bgcolor=ft.colors.WHITE,
            padding=0,
            controls=[
                ft.Row(
                    width=1000,
                    height=700,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                    controls=[
                        ft.Column(
                            width=100,
                            height=700,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                navigation,
                            ]
                        ),     
                        ft.Column(
                            width=900,
                            height=900,
                            spacing=0,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    height=90,
                                    controls=[
                                        ft.Text(value="Consultar Remessa", size=26, weight=ft.FontWeight.BOLD)
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Column(
                                            width=290,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=10,
                                            controls=[
                                                txtfield_buscaRemessa,
                                                btn_busca
                                            ]
                                        ),
                                        ft.Column(
                                            width=450,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    width=400,
                                                    height=150,
                                                    padding=0,
                                                    margin=ft.margin.all(10),
                                                    alignment=ft.alignment.top_left,
                                                    border=ft.border.all(1),
                                                    border_radius=ft.border_radius.all(10),
                                                    content=lv_resultadoBusca
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                                ft.Column(
                                    height=50,
                                    width=700,
                                    spacing=0,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Divider(),
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                    spacing=0,
                                    controls=[
                                        ft.Column(
                                            spacing=20,
                                            width=280,
                                            controls=[
                                                #COMARCA
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=2,
                                                            controls=[
                                                                ft.Text(value="Comarca", size=16, weight=ft.FontWeight.W_500),
                                                                txtfield_Comarca
                                                            ]
                                                        )
                                                    ]                                                    
                                                ),
                                                #RESPONSAVEL
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=2,
                                                            controls=[
                                                                ft.Text(value="Responsavel", size=16, weight=ft.FontWeight.W_500),
                                                                txtfield_Responsavel
                                                            ]
                                                        )
                                                    ]                                                    
                                                ),
                                                #REMESSA
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=2,
                                                            controls=[
                                                                ft.Text(value="Remessa", size=16, weight=ft.FontWeight.W_500),
                                                                txtfield_NumeroRemessa
                                                            ]
                                                        )
                                                    ]                                                    
                                                ),
                                                #DATA
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=2,
                                                            controls=[
                                                                ft.Text(value="Data", size=16, weight=ft.FontWeight.W_500),
                                                                txtfield_Data
                                                            ]
                                                        )
                                                    ]                                                    
                                                ),
                                                ]
                                        ),
                                        ft.Column(
                                            alignment=ft.MainAxisAlignment.START,
                                            spacing=20,
                                            width=200,
                                            controls=[
                                                #TOTAL
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=2,
                                                            controls=[
                                                                ft.Text(value="Total", size=16, weight=ft.FontWeight.W_500),
                                                                txtfield_Total
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                #TIPO
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=2,
                                                            controls=[
                                                                ft.Text(value="Tipo", size=16, weight=ft.FontWeight.W_500),
                                                                txtfield_Tipo
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                ft.Row(),
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=0,
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                            controls=[
                                                                ft.ElevatedButton(
                                                                    width=120,
                                                                    content=ft.Row(
                                                                        spacing=0,
                                                                        controls=
                                                                        [
                                                                            ft.Icon(name=ft.icons.PRINT, size=25),
                                                                            ft.Text(value="Imprmir", size=13),
                                                                        ],
                                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                                        
                                                                    ),
                                                                    style=ft.ButtonStyle(
                                                                        shape=ft.RoundedRectangleBorder(radius=10),
                                                                    ),
                                                                    bgcolor="#eeeeee",
                                                                    on_click=imprimir,
                                                                ),
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.START,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=0,
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                            controls=[
                                                                ft.ElevatedButton(
                                                                    width=120,
                                                                    content=ft.Row(
                                                                        spacing=0,
                                                                        controls=
                                                                        [
                                                                            ft.Icon(name=ft.icons.SAVE_OUTLINED, size=25),
                                                                            ft.Text(value="Salvar", size=13),
                                                                        ],
                                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                                        
                                                                    ),
                                                                    style=ft.ButtonStyle(
                                                                        shape=ft.RoundedRectangleBorder(radius=10),
                                                                    ),
                                                                    bgcolor="#eeeeee",
                                                                    on_click=salvarRemessa,
                                                                ),
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                
                                            ]
                                        ),           
                                        ft.Column(
                                            alignment=ft.MainAxisAlignment.START,
                                            horizontal_alignment=ft.MainAxisAlignment.START,
                                            spacing=0,
                                            controls=[
                                                ft.Text(value="Processos", size=16, weight=ft.FontWeight.W_500),
                                                ft.Container(
                                                    width=330,
                                                    height=280,
                                                    padding=0,
                                                    margin=ft.margin.all(10),
                                                    alignment=ft.alignment.top_left,
                                                    border=ft.border.all(1),
                                                    border_radius=ft.border_radius.all(10),
                                                    content=lv_procesos_da_remessa
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                                
                            ]
                        )
                    ],
                ),
            ]
        )

