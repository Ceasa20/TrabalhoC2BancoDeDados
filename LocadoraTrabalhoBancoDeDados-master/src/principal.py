from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_cliente import Controller_Cliente
from controller.controller_carro import Controller_Carro
from controller.controller_locacao import Controller_Locacao

# Inicialização dos componentes do sistema
relatorio = Relatorio()
ctrl_cliente = Controller_Cliente()
ctrl_carro = Controller_Carro()
ctrl_locacao = Controller_Locacao()


def reports(opcao_relatorio: str = "0"):
    acoes = {
        "1": relatorio.get_relatorio_carros,
        "2": relatorio.get_relatorio_locacao_por_carro,
        "3": relatorio.get_relatorio_clientes,
        "4": relatorio.get_relatorio_geral,
    }
    acao = acoes.get(opcao_relatorio)
    if acao:
        acao()


def inserir(opcao_inserir: str = "0"):
    acoes = {
        "1": ctrl_cliente.inserir_cliente,
        "2": ctrl_carro.inserir_carro,
        "3": ctrl_locacao.inserir_locacao,
    }
    acao = acoes.get(opcao_inserir)
    if acao:
        acao()


def atualizar(opcao_atualizar: str = "0"):
    acoes = {
        "1": (relatorio.get_relatorio_clientes, ctrl_cliente.atualizar_cliente),
        "2": (relatorio.get_relatorio_carros, ctrl_carro.atualizar_carro),
        "3": (relatorio.get_relatorio_locacao_por_carro, ctrl_locacao.atualizar_locacao),
    }
    for acao in acoes.get(opcao_atualizar, ()):
        acao()


def desativar_ou_finalizar(opcao: str = "0"):
    acoes = {
        "1": (relatorio.get_relatorio_clientes, ctrl_cliente.desativar_cliente),
        "2": (relatorio.get_relatorio_carros, ctrl_carro.desativar_carro),
        "3": (relatorio.get_relatorio_locacao_por_carro, ctrl_locacao.finalizar_locacao),
    }
    for acao in acoes.get(opcao, ()):
        acao()


def excluir_registro():
    acoes = {
        "1": ctrl_cliente.excluir_cliente,
        "2": ctrl_carro.excluir_carro,
        "3": ctrl_locacao.excluir_locacao,
    }
    print(config.MENU_ENTIDADES)
    opcao = config.solicitar_opcao(
        "Selecione a entidade que deseja excluir [0-3]: ",
        ("0", "1", "2", "3")
    )
    if opcao != "0":
        config.clear_console()
        acoes[opcao]()


def escolher_entidade(acao: str):
    """Menu comum para operações de cadastro; 0 sempre retorna ao menu anterior."""
    while True:
        print(config.MENU_ENTIDADES)
        opcao = config.solicitar_opcao(
            "Selecione [0-3]: ",
            ("0", "1", "2", "3")
        )

        if opcao == "0":
            return

        config.clear_console()

        if acao == "inserir":
            inserir(opcao)
        elif acao == "atualizar":
            atualizar(opcao)
        elif acao == "desativar":
            desativar_ou_finalizar(opcao)

        config.pausar()
        config.clear_console()


def run():
    while True:
        # A tela de resumo depende do banco Oracle; se a conexão falhar, o menu ainda deve abrir.
        try:
            print(SplashScreen().get_updated_screen())
        except Exception as erro:
            print(
                f"{config.YELLOW}Resumo do banco indisponível: "
                f"{erro}{config.RESET}"
            )
            print(
                "O menu será exibido mesmo assim. "
                "Verifique a conexão Oracle.\n"
            )

        print(config.MENU_PRINCIPAL)

        opcao = config.solicitar_opcao(
            "Escolha uma opção [0-5]: ",
            ("0", "1", "2", "3", "4", "5")
        )

        config.clear_console()

        if opcao == "1":
            while True:
                print(config.MENU_RELATORIOS)

                escolha = config.solicitar_opcao(
                    "Selecione um relatório [0-4]: ",
                    ("0", "1", "2", "3", "4")
                )

                if escolha == "0":
                    break

                config.clear_console()
                reports(escolha)

                # Os métodos de relatório já aguardam Enter; evita uma segunda pausa.
                config.clear_console()

        elif opcao == "2":
            escolher_entidade("inserir")

        elif opcao == "3":
            escolher_entidade("atualizar")

        elif opcao == "4":
            escolher_entidade("desativar")

        elif opcao == "5":
            excluir_registro()

        elif opcao == "0":
            print(
                f"\n{config.GREEN}"
                "Obrigado por utilizar o Sistema de Locação de Veículos."
                f"{config.RESET}"
            )
            break


if __name__ == "__main__":
    run()
