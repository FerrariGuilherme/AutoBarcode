
import flet as ft
import cryptocode
from flet_route import Params,Basket
from dependencias.database import bd

class AlteraUsuarioView:
    def __init__(self):
        ...

    def view(self,page:ft.page,params:Params,basket:Basket):

        ##
        #FUNCOES
        ##
        
        #Função para navegar entre as telas do menu de navegação
        def navChange(e):     
            if e == 0:
                navigation.on_change=page.go("/homeAdmProfile")

            if e == 1:
                navigation.on_change=page.go("/homeAdm")
            
            if e == 2:
                navigation.on_change=page.go("/")
        
        #Busca Usuario pelo ID
        def buscarUsuario(e):
            usuario = bd.consultar_database(f"SELECT * FROM users WHERE id = '{txtfield_id.value}'")
            if len(usuario) == 0:
                txtfield_id.error_text = "Não localizado"
            
            else:
                txtfield_nome.value = usuario[0][1]
                drop_Unidade.value = usuario[0][4]
                txtfield_email.value = usuario[0][2]
                txtfield_cpf.value = usuario[0][5]
                txtfield_id.error_text = None
            
            page.update()
        
        
        #Cadastrar novo usuario
        def alterarUsuario(e):
            
            txtfield_nome.error_text=None
            drop_Unidade.error_text=None
            txtfield_email.error_text=None
            txtfield_senha.error_text=None
            txtfield_cpf.error_text=None
            
            
            if txtfield_nome.value == "None" or txtfield_nome.value == "" or drop_Unidade.value == "None" or drop_Unidade.value == "" or txtfield_email.value == "None" or txtfield_email.value == "" or txtfield_senha.value == "None" or txtfield_senha.value == "" or txtfield_cpf.value == "None" or txtfield_cpf.value == "":
                
                if txtfield_nome.value == "None" or txtfield_nome.value == "":
                    txtfield_nome.error_text=" "
                    txtfield_nome.error_style=ft.TextStyle(size=0)
                    
                if drop_Unidade.value == "None" or drop_Unidade.value == "":
                    drop_Unidade.error_text=" "
                    drop_Unidade.error_style=ft.TextStyle(size=0)
                    
                if txtfield_email.value == "None" or txtfield_email.value == "":
                    txtfield_email.error_text=" "
                    txtfield_email.error_style=ft.TextStyle(size=0)
                    
                    
                if txtfield_senha.value == "None" or txtfield_senha.value == "":
                    txtfield_senha.error_text=" "
                    txtfield_senha.error_style=ft.TextStyle(size=0)
                    
                    
                if txtfield_cpf.value == "None" or txtfield_cpf.value == "":
                    txtfield_cpf.error_text=" "
                    txtfield_cpf.error_style=ft.TextStyle(size=0)

            else:
                id_usuario = int(txtfield_id.value)
                nome = txtfield_nome.value
                email = txtfield_email.value
                senha = txtfield_senha.value
                senha = cryptocode.encrypt(senha, 'Pge@123')
                cpf = txtfield_cpf.value
                unidade = drop_Unidade.value
                alterar_senha = switch_AlterarSenha.value
                
                #Função para feixar a caixa de dialogo - ('Usuario não confirmou cadastro')
                def close_dialog(e):
                    alert_dialog.open = False
                    page.update()
                
                #Função que realiza insert into no banco de dados - ('Usuario confirmou cadastro')
                def insert_user_bd(e):

                    #Criptografa a senha
                    
                    #Sobe a nova senha já criptografa para o bd
                    bd.alterar_database(f"UPDATE users SET nome='{nome}', email='{email}', password='{senha}', ambiente='{unidade}', cpf='{cpf}', reset_senha='{alterar_senha}' WHERE id='{id_usuario}'")
                    #Chama a função para fechar a caixa de dialogo
                    close_dialog(e)           
                    #Novo dialogo - Exibe sucesso na alteração de senha
                    dlg = ft.AlertDialog(
                        title=ft.Text("Alteração realizada com sucesso!"), on_dismiss=None
                    )
                    page.dialog = dlg
                    dlg.open = True
                    page.update()
                    
                #Dialogo - COnfirmação da alteração de senha
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("Alterar Usuario"),
                    content=ft.Text("Realmente deseja alterar od dados deste usuário"),
                    actions=[ft.TextButton("Sim", on_click=insert_user_bd), ft.TextButton("Não", on_click=close_dialog)],
                )
                #Exibe Dialogo
                page.dialog = alert_dialog
                alert_dialog.open = True
                page.update()

            page.update()
            
        #Ir para tela inicial
        def irParaTelaInicial(e):
            page.go('/homeAdm')

        ##
        #COMPONENTES
        ##
        
        navigation = ft.NavigationRail(
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
        
        btn_voltarI = ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT_OUTLINED,icon_size=30, tooltip="Voltar", on_click=irParaTelaInicial)
        
        txtfield_id = ft.TextField(label="ID do Usuário", hint_text="ID do Usuário", width=150, autofocus=True, input_filter= ft.NumbersOnlyInputFilter(), on_submit=buscarUsuario)
        btn_PesquisarId = ft.OutlinedButton(content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Text(value="Buscar", size=14, weight=ft.FontWeight.W_600)]), height=40, width=120, on_click=buscarUsuario)
        
        
        txtfield_nome = ft.TextField(label="Nome", hint_text="Nome do Colaborador", width=400, autofocus=True)
        drop_Unidade = ft.Dropdown(width=300, options=[ft.dropdown.Option("Sede - Pamplona"), ft.dropdown.Option("Procuradoria Fiscal"), ft.dropdown.Option("Administrador")], hint_text="Unidade/Ambiente")
        txtfield_email = ft.TextField(label="Email", hint_text="Email do Colaborador", width=400)
        txtfield_senha = ft.TextField(label="Senha", hint_text="Digite sua senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, autocorrect=True, autofocus=True, width=300)        
        txtfield_cpf = ft.TextField(label="CPF", hint_text="CPF do Colaborador", width=400)
        switch_AlterarSenha = ft.Switch(label="Alterar senha", value=True, scale=1.1, width=300)
        
        btn_voltarII = ft.OutlinedButton(content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Text(value="Voltar", size=18, weight=ft.FontWeight.W_600)]), height=50, width=250, on_click=irParaTelaInicial)
        btn_Atualizar = ft.FilledTonalButton(content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.Text(value="Atualizar", size=18, weight=ft.FontWeight.W_600)]), height=50, width=250, on_click=alterarUsuario)
        
        return ft.View(
            route="/alteraUsuario",
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
                            width=890,
                            height=700,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    height=20,
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        btn_voltarI
                                    ]
                                ),
                                ft.Row(
                                    height=90,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                    controls=[
                                        ft.Text(value="Alterar Usuário", size=42, width=ft.FontWeight.BOLD)
                                    ]                            
                                    ),
                                ft.Row(
                                    width=890,
                                    height=90,
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=60,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(width=2),
                                        txtfield_id,
                                        btn_PesquisarId
                                    ]
                                    ),
                                ft.Row(
                                    width=890,
                                    height=70,
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=60,
                                    vertical_alignment=ft.CrossAxisAlignment.END,
                                    controls=[
                                        ft.Container(width=2),
                                        txtfield_nome,
                                        drop_Unidade
                                    ]
                                    ),
                                ft.Row(
                                    width=890,
                                    height=70,
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=60,
                                    vertical_alignment=ft.CrossAxisAlignment.END,
                                    controls=[
                                        ft.Container(width=2),
                                        txtfield_email,
                                        txtfield_senha
                                    ]
                                    ),
                                ft.Row(
                                    width=890,
                                    height=70,
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=60,
                                    vertical_alignment=ft.CrossAxisAlignment.END,
                                    controls=[
                                        ft.Container(width=2),
                                        txtfield_cpf,
                                        switch_AlterarSenha
                                    ]
                                    ),
                                ft.Row(
                                    width=890,
                                    height=250,
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                    spacing=110,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        btn_voltarII,
                                        btn_Atualizar
                                    ]
                                )
                            ]
                        )
            ]
        )
            ]
        )
