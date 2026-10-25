MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Inativar Cadastros / Finalizar Locação
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de carros
2 - Relatório locação por carro
3 - Relatório de clientes
4 - Relatório geral
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - CLIENTES
2 - CARROS
3 - LOCACOES
"""

# Consulta de contagem de registros por tabela
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'

def solicitar_opcao(prompt: str, opcoes_validas: tuple) -> str:
    while True:
        opcao = input(prompt).strip()
        if opcao in opcoes_validas:
            return opcao
        print("Opção incorreta. Tente novamente.")


def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")