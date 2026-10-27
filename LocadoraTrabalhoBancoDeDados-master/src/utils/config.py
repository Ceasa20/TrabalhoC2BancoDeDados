"""Configurações e componentes de interface do terminal da locadora."""
import os
import sys
from time import sleep

# Cores ANSI (terminais modernos do Windows e Linux)
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

LARGURA_MENU = 80

MENU_PRINCIPAL = f"""
{CYAN}+==============================================================================+{RESET}
{CYAN}|{RESET}                    {BOLD}SISTEMA DE LOCAÇÃO DE VEÍCULOS{RESET}                       {CYAN}|{RESET}
{CYAN}+==============================================================================+{RESET}
{CYAN}|{RESET}  {GREEN}[1]{RESET}  Relatórios                                                            {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[2]{RESET}  Cadastrar novo registro                                               {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[3]{RESET}  Atualizar registro                                                    {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[4]{RESET}  Inativar cadastro / finalizar locação                                {CYAN}|{RESET}
{CYAN}|{RESET}  {RED}[0]{RESET}  Sair do sistema                                                       {CYAN}|{RESET}
{CYAN}+==============================================================================+{RESET}
"""

MENU_RELATORIOS = f"""
{CYAN}+==============================================================================+{RESET}
{CYAN}|{RESET}                              {BOLD}RELATÓRIOS{RESET}                                    {CYAN}|{RESET}
{CYAN}+==============================================================================+{RESET}
{CYAN}|{RESET}  {GREEN}[1]{RESET}  Relatório de veículos                                                  {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[2]{RESET}  Locações por veículo                                                   {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[3]{RESET}  Relatório de clientes                                                  {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[4]{RESET}  Relatório geral                                                        {CYAN}|{RESET}
{CYAN}|{RESET}  {YELLOW}[0]{RESET}  Voltar ao menu principal                                               {CYAN}|{RESET}
{CYAN}+==============================================================================+{RESET}
"""

MENU_ENTIDADES = f"""
{CYAN}+==============================================================================+{RESET}
{CYAN}|{RESET}                         {BOLD}SELECIONE O TIPO DE REGISTRO{RESET}                       {CYAN}|{RESET}
{CYAN}+==============================================================================+{RESET}
{CYAN}|{RESET}  {GREEN}[1]{RESET}  Clientes                                                               {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[2]{RESET}  Veículos                                                               {CYAN}|{RESET}
{CYAN}|{RESET}  {GREEN}[3]{RESET}  Locações                                                               {CYAN}|{RESET}
{CYAN}|{RESET}  {YELLOW}[0]{RESET}  Voltar ao menu principal                                               {CYAN}|{RESET}
{CYAN}+==============================================================================+{RESET}
"""

QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'


def solicitar_opcao(prompt: str, opcoes_validas: tuple) -> str:
    """Solicita uma opção até o usuário digitar uma das opções permitidas."""
    while True:
        try:
            opcao = input(f"{CYAN}{prompt}{RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{YELLOW}Operação cancelada.{RESET}")
            return "0" if "0" in opcoes_validas else opcoes_validas[-1]

        if opcao in opcoes_validas:
            return opcao

        print(
            f"\n{RED}[ERRO] Opção inválida.{RESET} "
            f"Escolha uma das opções: {', '.join(opcoes_validas)}.\n"
        )


def pausar(mensagem="Pressione Enter para continuar..."):
    """Mantém o resultado na tela até o usuário estar pronto para continuar."""
    try:
        input(f"\n{YELLOW}{mensagem}{RESET}")
    except (EOFError, KeyboardInterrupt):
        pass


def clear_console(wait_time: int = 0):
    """Limpa a tela no Windows ou Linux/macOS, opcionalmente após uma pausa."""
    if wait_time > 0:
        sleep(wait_time)

    os.system("cls" if os.name == "nt" else "clear")
