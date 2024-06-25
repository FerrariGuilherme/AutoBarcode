from flet_route import Params,Basket
from dependencias.database import bd
import flet as ft
import pickle
import cryptocode

class AlteraSenha:
    def __init__(self):
        ...

    def view(self,page:ft.page,params:Params,basket:Basket):
        
        ##
        #FUNCOES
        ##
        
        #Carrega arquivo de log - login_data.pkl
        with open("login_data.pkl", "rb") as file:
            log = pickle.load(file)
        

        def irParatelaHome(e):
            if log[0][4] == "Administrador":
                page.go('/homeAdm')   
            else: 
                page.go('/home')
           
        #Altera senha do usuario
        def reset_password(e):
            
            #Coleta as values dos campos de alterar senha
            pass_new = txt_pass_new.value
            pass_new_reconfirm = txt_pass_new_reconfirm.value
            
            #Define as msg de erro como None
            txt_pass_new.error_text = None
            txt_pass_new_reconfirm.error_text = None
            page.update()
            
            #Verificar se os campos necessarios estão em branco - Só ira prosseguir se todos os campos forem diferentes de "VAZIO"
            if pass_new != '' and pass_new_reconfirm != '':

                #Compara se a value da entry 'Nova Senha' é igual a 'Confirme nova senha' - True entra no elif e exibe msg de erro nas duas entrys
                if pass_new != pass_new_reconfirm:
                    txt_pass_new.error_text = "As senhas não coincidem"
                    txt_pass_new_reconfirm.error_text = "As senhas não coincidem"
                    page.update()
                
                #Se for igual entra no else para fazer o update no bd
                else:
                    
                    ##
                    #CAIXA DE DIALOGO
                    #
                    
                    #Função para feixar a caixa de dialogo - ('Usuario não confirmou alteração de senha')
                    def close_dialog(e):
                        alert_dialog.open = False
                        
                        txt_pass_new.value = ""
                        txt_pass_new_reconfirm.value = ""
                       
                        txt_pass_new.focus()
                        page.update()
                    
                    #Função que realiza update de password no banco de dados - ('Usuario confirmou alteração de senha')
                    def update_pass_bd(e):
                        pass_new = txt_pass_new.value
                        #Criptografa a nova senha
                        pass_new = cryptocode.encrypt(pass_new, 'Pge@123')
                        #Sobe a nova senha já criptografa para o bd
                        bd.alterar_database(f"UPDATE users SET password = '{pass_new}', reset_senha = 'False' WHERE id = {log[0][0]}")
                        #Chama a função para fechar a caixa de dialogo
                        close_dialog(e)
                        
                        #Novo dialogo - Exibe sucesso na alteração de senha
                        dlg = ft.AlertDialog(
                            title=ft.Text("Senha alterada com sucesso!"), on_dismiss=None
                        )
                        page.dialog = dlg
                        dlg.open = True
                        
                        btn_resetPass.disabled=True
                        btn_continuar.disabled=False                    
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
                page.update()
            
        #Focus txt_pass_new_reconfirm
        def focus_reconfirm(e):
            txt_pass_new_reconfirm.focus()
            
            
        ##
        #COMPONENTES
        ##
        

       
        txt_nome = ft.TextField(label="Nome completo", read_only=True, value=f"{log[0][1]}", width=450, icon=ft.icons.PERSON_PIN, height=50, content_padding=ft.padding.only(10, 0, 0, 0))
        txt_id = ft.TextField(label="ID", read_only=True, value=f"{log[0][0]}", width=120, icon=ft.icons.GRID_3X3_OUTLINED, height=50, content_padding=ft.padding.only(10, 0, 0, 0))
        txt_email = ft.TextField(label="Email", read_only=True, value=f"{log[0][2]}", width=450, icon=ft.icons.EMAIL, height=50, content_padding=ft.padding.only(10, 0, 0, 0))
        txt_ambiente = ft.TextField(label="Ambiente", read_only=True, value=f"{log[0][4]}", width=450, icon=ft.icons.LOCATION_CITY, height=50, content_padding=ft.padding.only(10, 0, 0, 0))
        
        
        txt_pass_new = ft.TextField(label="Nova Senha", hint_text="Digite a nova senha", width=280, password=True, can_reveal_password=True, prefix_icon=ft.icons.PASSWORD, autofocus=True, on_submit=focus_reconfirm)
        txt_pass_new_reconfirm = ft.TextField(label="Confirme nova senha", hint_text="Digite novamente a nova senha", width=280, password=True, can_reveal_password=True, prefix_icon=ft.icons.PASSWORD, autofocus=True, on_submit=reset_password)
        
        btn_resetPass = ft.ElevatedButton(text="Alterar Senha", height=40, width=220, on_click=reset_password)
        
        btn_continuar = ft.ElevatedButton(text="Continuar", height=40, width=220, on_click=irParatelaHome, disabled=True)
        

        return ft.View(
            route="/alteraSenha",
            bgcolor=ft.colors.WHITE,
            padding=0,
            controls=[
                ft.Row(
                    width=1000,
                    height=700,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=100,
                    controls=[    
                        ft.Column(
                            width=700,
                            height=700,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[

                                ft.Column(
                                    controls=[
                                        ft.Row(height=10),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=250,
                                            controls=[
                                                ft.Text(value="Altere sua senha", weight=ft.FontWeight.W_300, size=22)
                                            ]
                                        ),
                                        ft.Row(height=25),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.START,
                                            spacing=30,
                                            controls=[
                                                ft.Column(
                                                    spacing=15,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        txt_pass_new,
                                                        txt_pass_new_reconfirm,
                                                        
                                                    ]
                                                ),
                                            ]    
                                        ),
                                        ft.Row(height=20),
                                        ft.Row(
                                            spacing=15,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                btn_resetPass,
                                                btn_continuar
                                            ]
                                        ),
                                        ft.Row(height=30),
                                        ft.Divider(color="black",),
                                        ft.Row(height=20),
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
                                    ]
                                ),
                            ]
                        )
                    ],
                ),
            ]
        )
