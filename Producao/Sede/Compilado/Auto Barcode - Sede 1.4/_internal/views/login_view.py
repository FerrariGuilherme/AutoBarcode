import flet as ft
import cryptocode
import pickle
from dependencias.apotamento_ambiente import ambiente
from flet_route import Params,Basket 
from time import sleep
from dependencias.database import bd

#Tela de login
class LoginView:
    def __init__(self):
        ...

    #Componentes
    def view(self,page:ft.page,params:Params,basket:Basket):
        
        versao = "1.4"
        atual = ""
        if bd.consultar_database("SELECT * FROM versionamento WHERE atual = 'True'")[0][0] != versao:
            txtfield_email.read_only = True
            txtfield_senha.read_only = True
            atual = "Versão Desatualizada"
            
        else:
            atual = ""   
        
        # Ação para liberar login
        def login(e):
            
            #Coleta email e senha
            login = txtfield_email.value
            password = txtfield_senha.value
            
            #Busca no Banco de dados o email e registra o retorno na variavel verifica_login
            verifica_login = bd.consultar_database(f"SELECT * FROM users WHERE email = '{login}'")
            
            #Se não achar o email no banco de dados o retorno o 0 // Se achar mais de uma linha com o mesmo email tambem da erro, porque não devera acontecer isso, email é unico para cada usuario

            #Validação retorno da variavel verifica_login igual a 0 ou mais de 1            
            if len(verifica_login) == 0:
                #Exibe erro nos campos txtfield_email // txtfield_senha
                txtfield_email.error_text = " "
                
                txtfield_senha.error_text = "Usuario não encontrado"
                page.update()
                
            elif len(verifica_login) > 1:
                #Exibe erro nos campos txtfield_email // txtfield_senha
                txtfield_email.error_text = " "
                
                txtfield_senha.error_text = "Erro na base"
                page.update()
            
            #Validação retorno da variavel verifica_login igual a 1 - IDEAL
            elif len(verifica_login) == 1:
                # Email localizado com sucesso // email do usuario localizado.
                
                #Descriptografa a senha que esta no banco de dados e compara com a senha informada no txtfield_senha
                if cryptocode.decrypt(verifica_login[0][3], "Pge@123") == password:
                    #Senha iguais / Sucesso na autenticação
                    txtfield_email.error_text = ""
                    txtfield_senha.error_text = ""
                    page.update()
                    
                    #Escreve no arquivo cache de login
                    with open("login_data.pkl", "wb") as file:
                        pickle.dump(verifica_login, file)

                    #Direciona para tela HOME
                    #Verifica se usuario que logou é ADM
                    if verifica_login[0][6] == 'True':
                        page.go('/alteraSenha')
                        
                    elif verifica_login[0][4] == 'Administrador':
                        page.go('/homeAdm')
                    else:
                        page.go('/home')
                    
                else:
                    #Senha incorreta
                    
                    #Exibe erro nos campos txtfield_email // txtfield_senha
                    txtfield_email.error_text = " "
                    txtfield_senha.error_text = "Email ou senha invalidos"
                    page.update()
                
            #Validação retorno da variavel verifica_login qualquer outro resultado diferente aos de cima.  
            else:
                #Exibe erro nos campos txtfield_email // txtfield_senha
                txtfield_email.error_text = " "
                txtfield_senha.error_text = "Email ou senha invalidos"
                page.update()
            
        #Função para jogar o focus para o campo de senha ao pressionar 'Enter' no campo de email
        def on_focus_password(e):
            txtfield_senha.focus()
        

                
        #Componentes de email / senha
        txtfield_email = ft.TextField(label="Email", hint_text="Digite seu email", width=350, prefix_icon=ft.icons.ALTERNATE_EMAIL, autocorrect=True, autofocus=True, on_submit=on_focus_password)
        txtfield_senha = ft.TextField(label="Senha", hint_text="Digite sua senha",password=True, can_reveal_password=True, width=350, prefix_icon=ft.icons.LOCK, autocorrect=True, autofocus=True, on_submit=login)

        #Botão Entrar
        btn_entrar = ft.ElevatedButton(text="Entrar", width=250, height=40, on_click=login) #login

        #Visualização dos componentes.
        return ft.View(
            route= "/",
            bgcolor=ft.colors.WHITE,
            padding=0,
            controls=[
                
                # Layout principal (Row) Horizontal
                ft.Row(
                    width=1000,
                    height=700,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        #Dentro da (ROW) tem duas Column Vertical
                        
                        #Primeira Column
                        ft.Column(
                            height=800,
                            width=600,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            #Dentro da primeira Column - Tem a Imagem
                            controls=[
                                ft.Image(
                                    src="..\\assets\\12.png",
                                    height=600,
                                    fit=ft.ImageFit.COVER,
                                    )
                            ],
                        ),
                        
                        #Segunda Column
                        ft.Column(
                            height=800,
                            width=300,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                #Dentro da segunda Column os campos para realizar login
                                ft.Text(value="Fazer login", italic=False, selectable=False, style='displaySmall'),
                                ft.Row(height=50),
                                txtfield_email,
                                txtfield_senha,
                                ft.Row(height=20),
                                btn_entrar,
                                ft.Text(value="", size=20,),
                                ft.Text(value=f"Versão {versao} - {ambiente}  ©", italic=True, selectable=False, style='displaySmall', size=12, weight=ft.FontWeight.W_600, color="#777777"),
                                ft.Text(value=f"{atual}", italic=True, selectable=False, style='displaySmall', size=12, weight=ft.FontWeight.W_600, color="#777777"),
                            ],
                        ),
                    ]
                )
            ]
        )
       
       
