from flet_route import Params,Basket
from dependencias.database import bd
import flet as ft
import pickle
import cryptocode

class HomeProfile:
    def __init__(self):
        ...

    def view(self,page:ft.page,params:Params,basket:Basket):
        
        ##
        #FUNCOES
        ##
        
        #Carrega arquivo de log - login_data.pkl
        with open("login_data.pkl", "rb") as file:
            log = pickle.load(file)
        
        #Função para navegar entre as telas do menu de navegação
        def navChange(e):     
            if e == 0:
                pass
                
            if e == 1:
                navigation.on_change=page.go("/home")
            
            if e == 2:
                navigation.on_change=page.go("/")
    
        #Altera senha do usuario
        def reset_password(e):
            
            #Coleta as values dos campos de alterar senha
            pass_new = txt_pass_new.value
            pass_new_reconfirm = txt_pass_new_reconfirm.value
            passAtual = txt_passAtual.value
            
            #Define as msg de erro como None
            txt_pass_new.error_text = None
            txt_pass_new_reconfirm.error_text = None
            txt_passAtual.error_text = None
            page.update()
            
            #Verificar se os campos necessarios estão em branco - Só ira prosseguir se todos os campos forem diferentes de "VAZIO"
            if pass_new != '' and pass_new_reconfirm != '' and passAtual != '':
                
                #Busca no bd a password do usuario atraves id, id coletado no arq de log
                senha_atual_BD = bd.consultar_database(f"SELECT password FROM users WHERE id = {log[0][0]}")
                
                #Descriptografa a senha do banco de dados
                senha_atual_BD = cryptocode.decrypt(senha_atual_BD[0][0], 'Pge@123')
                
                #Compara se a senha desciptografada do bd é diferente a value do campo 'Senha Atual' - True, entra no if e exibe msg de erro na entry 'Senha Atual'
                if senha_atual_BD != passAtual:
                    txt_passAtual.error_text = "Campo invalido"
                    page.update()
                
                #Compara se a value da entry 'Nova Senha' é igual a 'Confirme nova senha' - True entra no elif e exibe msg de erro nas duas entrys
                elif pass_new != pass_new_reconfirm:
                    txt_pass_new.error_text = "Campo invalido"
                    txt_pass_new_reconfirm.error_text = "Campo invalido"
                    page.update()
                
                #Não entrou em nenhum dos IF's a cima, entra no else para fazer o update no bd
                else:
                    
                    ##
                    #CAIXA DE DIALOGO
                    #
                    
                    #Função para feixar a caixa de dialogo - ('Usuario não confirmou alteração de senha')
                    def close_dialog(e):
                        alert_dialog.open = False
                        
                        txt_pass_new.value = ""
                        txt_pass_new_reconfirm.value = ""
                        txt_passAtual.value = ""
                        
                        page.update()
                    
                    #Função que realiza update de password no banco de dados - ('Usuario confirmou alteração de senha')
                    def update_pass_bd(e):
                        pass_new = txt_pass_new.value
                        #Criptografa a nova senha
                        pass_new = cryptocode.encrypt(pass_new, 'Pge@123')
                        #Sobe a nova senha já criptografa para o bd
                        bd.alterar_database(f"UPDATE users SET password = '{pass_new}' WHERE id = {log[0][0]}")
                        #Chama a função para fechar a caixa de dialogo
                        close_dialog(e)
                        
                        #Novo dialogo - Exibe sucesso na alteração de senha
                        dlg = ft.AlertDialog(
                            title=ft.Text("Senha alterada com sucesso!"), on_dismiss=None
                        )
                        page.dialog = dlg
                        dlg.open = True
                        page.update()
                        
                    #Dialogo - COnfirmação da alteração de senha
                    alert_dialog = ft.AlertDialog(
                        title=ft.Text("Alterar senha"),
                        content=ft.Text("Realmente deseja aterar sua Senha ?"),
                        actions=[ft.TextButton("Sim", on_click=update_pass_bd), ft.TextButton("Não", on_click=close_dialog)],
                    )
                    #Exibe Dialogo
                    page.dialog = alert_dialog
                    alert_dialog.open = True
                    page.update()
                    
            #Se algum dos campos estiverem vazios, exibe msg de erro nas entrys
            else:
                txt_pass_new.error_text = "Campo invalido"
                txt_pass_new_reconfirm.error_text = "Campo invalido"
                txt_passAtual.error_text = "Campo invalido"
                page.update()
            
            
        ##
        #COMPONENTES
        ##
        
        #Menu de navegação
        navigation = ft.NavigationRail(
                            selected_index=0,
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

        txt_nome = ft.TextField(label="Nome completo", read_only=True, value=f"{log[0][1]}", width=450, icon=ft.icons.PERSON_PIN)
        txt_id = ft.TextField(label="ID", read_only=True, value=f"{log[0][0]}", width=120, icon=ft.icons.GRID_3X3_OUTLINED)
        txt_email = ft.TextField(label="Email", read_only=True, value=f"{log[0][2]}", width=450, icon=ft.icons.EMAIL)
        txt_ambiente = ft.TextField(label="Ambiente", read_only=True, value=f"{log[0][4]}", width=450, icon=ft.icons.LOCATION_CITY)
        
        txt_passAtual = ft.TextField(label="Senha atual", hint_text="Digite sua senha atual", width=280, password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK_OUTLINED, autofocus=True)
        txt_pass_new = ft.TextField(label="Nova Senha", hint_text="Digite a nova senha", width=280, password=True, can_reveal_password=True, prefix_icon=ft.icons.PASSWORD, autofocus=True)
        txt_pass_new_reconfirm = ft.TextField(label="Confirme nova senha", hint_text="Digite novamente a nova senha", width=280, password=True, can_reveal_password=True, prefix_icon=ft.icons.PASSWORD, autofocus=True)
        
        btn_resetPass = ft.ElevatedButton(text="Alterar Senha", height=40, width=220, on_click=reset_password)
        

        return ft.View(
            route="/homeProfile",
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
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(height=10),
                                ft.Text(value="Dados Usuário", size=48, weight=ft.FontWeight.W_300),
                                ft.Row(height=30),
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=250,
                                            controls=[
                                                txt_nome,
                                                txt_id
                                            ]
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=250,
                                            controls=[
                                                txt_email
                                            ]
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=250,
                                            controls=[
                                                txt_ambiente
                                            ]
                                        ),
                                        ft.Row(height=10),
                                        ft.Divider(color="black",),
                                        ft.Row(height=10),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=250,
                                            controls=[
                                                ft.Text(value="Alterar senha", weight=ft.FontWeight.W_300, size=22)
                                            ]
                                        ),
                                        ft.Row(height=10),
                                        ft.Row(
                                            vertical_alignment=ft.CrossAxisAlignment.START,
                                            spacing=30,
                                            controls=[
                                                ft.Column(
                                                    spacing=15,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        txt_pass_new,
                                                        txt_pass_new_reconfirm
                                                    ]
                                                ),
                                                ft.Column(
                                                    spacing=15,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        txt_passAtual,
                                                        btn_resetPass
                                                    ]
                                                ),
                                                
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
