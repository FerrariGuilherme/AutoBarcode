from flet_route import Params,Basket
from dependencias.database import bd
import flet as ft
import pickle
import cryptocode

class HistoricoView:
    def __init__(self):
        ...

    def view(self,page:ft.page,params:Params,basket:Basket):
        
        ##
        #VARIAVEIS
        ##
        
        
        
        
        ##
        #FUNCOES
        ##
        
        #Carrega arquivo de log - login_data.pkl
        with open("login_data.pkl", "rb") as file:
            log = pickle.load(file)
        
        #Função para navegar entre as telas do menu de navegação
        def navChange(e):     
            if e == 0:
                navigation.on_change=page.go("/homeProfile")
                
            if e == 1:
                navigation.on_change=page.go("/home")
            
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
    
        def radiogroup_changed(e):
            lv_historico.controls.clear()
            historico = bd.consultar_database(f"SELECT historico FROM 'processos.historico' WHERE processo = '{e.control.value}'")
            historico = ft.Text(value=historico[0][0], selectable=True)
            lv_historico.controls.append(historico)
            page.update()
            

    
        def coletaProcessos(e):
            caixaDeDialogoSimples(titulo="Pesquisando processo", content=ft.ProgressBar(color="amber", bgcolor="#eeeeee"))
            lista_de_processos.controls.clear()
            if txtfield_buscaProcesso.value == None:
                processos = bd.consultar_database(f"SELECT processo FROM 'processos.historico' WHERE processo LIKE '%%';")
            else:
                processos = bd.consultar_database(f"SELECT processo FROM 'processos.historico' WHERE processo LIKE '%{txtfield_buscaProcesso.value}%';")
            for processo in processos:
                lista_de_processos.controls.append(ft.Radio(value=f"{processo[0]}", label=f"{processo[0]}"))
            page.dialog.open=False
            txtfield_buscaProcesso.focus()
            page.update()
            
        ##
        #COMPONENTES
        ##
        
        txtfield_buscaProcesso = ft.TextField(label="Numero do processo", prefix_icon=ft.icons.NUMBERS, hint_text="xxxxxxx-xx.xxxx.x.xx.xxxx", width=350, on_submit=coletaProcessos)
        btn_busca =  ft.IconButton(icon=ft.icons.SEARCH, tooltip="Buscar", on_click=coletaProcessos)
        
        lista_de_processos = ft.Column(spacing=0,controls=[])
        
        #radio_group = ft.RadioGroup(content=lista_de_processos, on_change=radiogroup_changed)
        lv_resultadoBusca = ft.ListView(width=500, height=150, controls=[ft.RadioGroup(content=lista_de_processos, on_change=radiogroup_changed)])
        
        lv_historico = ft.ListView(width=750, height=300, padding=5, disabled=False, )
        
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
            route="/Historico",
            bgcolor=ft.colors.WHITE,
            padding=0,
            controls=[
                ft.Row(
                    width=1000,
                    height=700,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=100,
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
                            width=700,
                            height=700,
                            spacing=0,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    height=90,
                                    controls=[
                                        ft.Text(value="HISTORICO", size=26, weight=ft.FontWeight.BOLD)
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        txtfield_buscaProcesso,
                                        btn_busca
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            width=700,
                                            height=300,
                                            alignment=ft.alignment.top_left,
                                            border=ft.border.all(1),
                                            border_radius=ft.border_radius.all(10),
                                            content=lv_historico
                                        )
                                    ]
                                ),
                                
                            ]
                        )
                    ],
                ),
            ]
        )
