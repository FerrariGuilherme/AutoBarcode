import flet as ft
import pickle
from dependencias.database import bd
from flet_route import Params,Basket 

class HomeView:
    def __init__(self):
        ...
        
    def view(self,page:ft.page,params:Params,basket:Basket):
        
        ##
        #FUNCOES
        ##
        
        #Leitura do log // login_data.pkl 
        with open("login_data.pkl", "rb") as file:
            query_login = pickle.load(file)
        
        #Função para navegar entre as telas do menu de navegação
        def navChange(e):     
            if e == 0:
                navigation.on_change=page.go("/homeProfile")

            if e == 1:
                pass
            
            if e == 2:
                navigation.on_change=page.go("/")
        
        def irParaTelaRegistrarEntrada(e):
            page.go('/registroEntrada')
            
        def irParaTelaRegistrarSaida(e):
            page.go('/registroSaida')
            
        def irParaTelaRegistrarDigitalizacao(e):
            page.go('/registroDigitalizacao')
            
        def irParaTelaHistorico(e):
            page.go('/Historico')
            
        def irParaTelaConsultarRemessa(e):
            page.go('/consultarRemessa')
        
        ##
        #COMPONENTES
        ##
        
        #Menu de navegação
        navigation = ft.NavigationRail(
                            selected_index=1,
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
            route="/home",
            bgcolor=ft.colors.WHITE,
            padding=0,
            controls=[
                ft.Row(
                    width=1000,
                    height=700,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(
                            width=110,
                            height=700,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                navigation,
                            ],
                        ),
                        
                        ft.Column(
                            width=865,
                            height=700,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    height=300,
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Row(
                                                    height=100,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Icon(name=ft.icons.PERSON_OUTLINED, size=45),
                                                        ft.Text(value=f"{query_login[0][1]}", size=22, weight=ft.FontWeight.W_400),
                                                    ]
                                                )
                                            ]
                                            ),
                                        ft.Column(
                                            controls=[
                                                ft.Row(
                                                    height=100,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Icon(name=ft.icons.HOME_WORK_OUTLINED, size=45),
                                                        ft.Text(value=f"{query_login[0][4]}", weight=ft.FontWeight.W_700, size=22),
                                                    ]
                                                )
                                            ]
                                            ),
                                        
                                    ]
                                ),
                                ft.Row(
                                    width=700,
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.OutlinedButton(text="Registrar Entrada", on_click=irParaTelaRegistrarEntrada, height=50, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
                                        ft.OutlinedButton(text="Digitalização", on_click=irParaTelaRegistrarDigitalizacao, height=50, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
                                        
                                        ],
                                    ),
                                ft.Row(
                                    height=50,
                                    width=700,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.OutlinedButton(text="Historico",on_click=irParaTelaHistorico, height=50, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
                                        
                                        ],
                                    ),
                                ft.Row(
                                    width=700,
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.OutlinedButton(text="Registrar Saída", on_click=irParaTelaRegistrarSaida, height=50, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
                                        ft.OutlinedButton(text="Consultar Remessa", on_click=irParaTelaConsultarRemessa, height=50, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
                                        
                                        ],
                                    ),
                                
                                ft.Row(),
                                ],  
                        )
                        ],
                ),
            ]
        )
        

