from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_carro import Controller_Carro
from controller.controller_cliente import Controller_Cliente
from controller.controller_locacao import Controller_Locacao


tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_carro = Controller_Carro()
ctrl_cliente = Controller_Cliente()
ctrl_locacao = Controller_Locacao()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_pedidos_por_fornecedor()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_pedidos()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_produtos()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_clientes()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_fornecedores()
    elif opcao_relatorio == 6:
        relatorio.get_relatorio_itens_pedidos()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_carro = ctrl_carro.inserir_carro()
    elif opcao_inserir == 2:
        novo_cliente = ctrl_cliente.inserir_cliente()
    elif opcao_inserir == 3:
        novo_locacao = ctrl_locacao.inserir_locacao()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_produtos()
        produto_atualizado = ctrl_produto.atualizar_produto()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_clientes()
        cliente_atualizado = ctrl_cliente.atualizar_cliente()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_fornecedores()
        fornecedor_atualizado = ctrl_fornecedor.atualizar_fornecedor()
    elif opcao_atualizar == 4:
        relatorio.get_relatorio_pedidos()
        pedido_atualizado = ctrl_pedido.atualizar_pedido()
    elif opcao_atualizar == 5:
        relatorio.get_relatorio_itens_pedidos()
        item_pedido_atualizado = ctrl_item_pedido.atualizar_item_pedido()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_produtos()
        ctrl_produto.excluir_produto()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_clientes()
        ctrl_cliente.excluir_cliente()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_fornecedores()
        ctrl_fornecedor.excluir_fornecedor()
    elif opcao_excluir == 4:                
        relatorio.get_relatorio_pedidos()
        ctrl_pedido.excluir_pedido()
    elif opcao_excluir == 5:
        relatorio.get_relatorio_itens_pedidos()
        ctrl_item_pedido.excluir_item_pedido()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-6]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()