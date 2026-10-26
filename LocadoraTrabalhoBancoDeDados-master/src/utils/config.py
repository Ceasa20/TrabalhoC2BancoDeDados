
MENU_PRINCIPAL = """
+==================================================================+
|                         MENU PRINCIPAL                           |
+==================================================================+
|  1 - Relatórios                                                  |
|  2 - Inserir registros                                           |
|  3 - Atualizar registros                                         |
|  4 - Inativar cadastros / Finalizar locação                      |
|  5 - Sair                                                        |
+==================================================================+
"""

MENU_RELATORIOS = """
+==================================================================+
|                           RELATÓRIOS                             |
+==================================================================+
|  1 - Relatório de carros                                         |
|  2 - Relatório de locação por carro                              |
|  3 - Relatório de clientes                                       |
|  4 - Relatório geral                                             |
|  0 - Sair                                                        |
+==================================================================+
"""

MENU_ENTIDADES = """
+==================================================================+
|                           ENTIDADES                              |
+==================================================================+
|  1 - CLIENTES                                                    |
|  2 - CARROS                                                      |
|  3 - LOCACOES                                                    |
+==================================================================+
"""

# Consulta de contagem de registros por tabela
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'


def solicitar_opcao(prompt: str, opcoes_validas: tuple) -> str:
    while True:
        opcao = input(prompt).strip()
        if opcao in opcoes_validas:
            return opcao
        print("\n[!] Opção incorreta. Escolha uma das opções do menu.\n")


def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")
