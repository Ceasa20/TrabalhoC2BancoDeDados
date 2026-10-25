from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_produto import Controller_Produto
from controller.controller_cliente import Controller_Cliente
from controller.controller_fornecedor import Controller_Fornecedor
from controller.controller_pedido import Controller_Pedido
from controller.controller_item_pedido import Controller_Item_Pedido

# Inicialização da splash screen, relatórios e das controllers
tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_produto = Controller_Produto()
ctrl_cliente = Controller_Cliente()
ctrl_fornecedor = Controller_Fornecedor()
ctrl_pedido = Controller_Pedido()
ctrl_item_pedido = Controller_Item_Pedido()

def reports(opcao_relatorio: int = 0):
    if opcao_relatorio == 1:
        relatorio.get_relatorio_locacoes()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_clientes()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_carros()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_produto = ctrl_produto.inserir_produto()
    elif opcao_inserir == 2:
        novo_cliente = ctrl_cliente.inserir_cliente()
    elif opcao_inserir == 2:
        novo_carro = ctrl_carro.inserir_carro()
    elif opcao_inserir == 3:
        novo_fornecedor = ctrl_fornecedor.inserir_fornecedor()
    elif opcao_inserir == 4:
        novo_pedido = ctrl_pedido.inserir_pedido()
    elif opcao_inserir == 5:
        novo_item_pedido = ctrl_item_pedido.inserir_item_pedido()

def atualizar(opcao_atualizar: int = 0):
    if opcao_atualizar == 1:
        relatorio.get_relatorio_clientes()
        cliente_atualizado = ctrl_cliente.atualizar_cliente()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_carros()
        carro_atualizado = ctrl_carro.atualizar_carro()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_locacoes()
        locacao_atualizada = ctrl_locacao.atualizar_locacao()

def excluir(opcao_excluir: int = 0):
    if opcao_excluir == 1:
        relatorio.get_relatorio_clientes()
        ctrl_cliente.excluir_cliente()
    elif opcao_excluir == 2:
        relatorio.get_relatorio_carros()
        ctrl_carro.excluir_carro()
    elif opcao_excluir == 3:
        relatorio.get_relatorio_locacoes()
        ctrl_locacao.excluir_locacao()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros
            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4: # Excluir Registros
            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5: # Sair
            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()
