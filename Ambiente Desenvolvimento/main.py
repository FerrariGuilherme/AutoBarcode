import flet as ft
from flet_route import Routing,path
from views.login_view import LoginView 
from views.Principal.alteraSenha_view import AlteraSenha
from views.Principal.home_view import HomeView 
from views.Principal.homeProfile_view import HomeProfile
from views.Adm.homeAdm_view import HomeAdmView
from views.Adm.homeAdmProfile_view import HomeAdmProfile
from views.Adm.cadastro_view import CadastroView
from views.Adm.alterar_usuario import AlteraUsuarioView
from views.Registros.registroEntrada_view import EntradaView
from views.Registros.registroSaida_view import SaidaView
from views.Registros.registroDigitalizacao_view import DigitalizacaoView
from views.Registros.registroDistribuicao_view import DistribuicaoView
from views.Registros.historico_view import HistoricoView
from views.Registros.consultar_remessa import ConsultarRemessa




def main(page: ft.Page):
    page.title = "AutoBarcode"
    page.window_height = 700
    page.window_width = 1000
    page.window_resizable = False
    page.window_maximizable = False
    page.window_center()
    page.theme_mode = ft.ThemeMode.LIGHT

    
    

    app_routes = [
        path(url="/", clear=True, view=LoginView().view),
        path(url="/alteraSenha", clear=False, view=AlteraSenha().view),
        path(url="/home", clear=False, view=HomeView().view),
        path(url="/homeProfile", clear=False, view=HomeProfile().view),
        path(url="/homeAdm", clear=False, view=HomeAdmView().view),
        path(url="/homeAdmProfile", clear=False, view=HomeAdmProfile().view),
        path(url="/cadastro", clear=False, view=CadastroView().view),
        path(url="/alteraUsuario", clear=False, view=AlteraUsuarioView().view),
        path(url="/registroEntrada", clear=False, view=EntradaView().view),
        path(url="/registroSaida", clear=False, view=SaidaView().view),
        path(url="/registroDigitalizacao", clear=False, view=DigitalizacaoView().view),
        path(url="/registroDistribuicao", clear=False, view=DistribuicaoView().view),
        path(url="/Historico", clear=False, view=HistoricoView().view),
        path(url="/consultarRemessa", clear=False, view=ConsultarRemessa().view),
    ]

    Routing(
        page=page, 
        app_routes=app_routes, 
        )
    page.go(page.route)

ft.app(target=main)