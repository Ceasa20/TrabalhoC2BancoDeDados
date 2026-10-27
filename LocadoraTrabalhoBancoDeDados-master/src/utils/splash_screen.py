from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_carros = config.QUERY_COUNT.format(tabela="carros")
        self.qry_total_clientes = config.QUERY_COUNT.format(tabela="clientes")
        self.qry_total_locacao = config.QUERY_COUNT.format(tabela="locacao")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = """Cesar Peixoto Silva - 25110729 
                    Daniel Stieg Radaelle  - 25110517
                    Gabriel Malheiros de Castro - 23110145
                    Lucas de Souza Barboza - 25110593
                    Enzo Ceglias Coutinho - 25110519
                    Arthur Nunes Berti Xavier - 25110636"""
        self.disciplina = "Banco de Dados"
        self.semestre = "2026/2"

    def get_total_carros(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_carros)["total_carros"].values[0]

    def get_total_clientes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_clientes)["total_clientes"].values[0]

    def get_total_locacao(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_locacao)["total_locacao"].values[0]


    def get_updated_screen(self):
        # Monta a tela inicial com os totais de registros do banco
        largura = 68
        borda = "+" + "=" * (largura - 2) + "+"
        separador = "+" + "-" * (largura - 2) + "+"

        def linha(texto=""):
            conteudo = str(texto)[:largura - 4]
            return "| " + conteudo.center(largura - 4) + " |"

        linhas = [
            borda,
            linha("SISTEMA DE LOCAÇÃO DE VEÍCULOS"),
            borda,
            linha("RESUMO DE REGISTROS"),
            separador,
            linha(f"CARROS CADASTRADOS: {self.get_total_carros()}"),
            linha(f"CLIENTES CADASTRADOS: {self.get_total_clientes()}"),
            linha(f"LOCAÇÕES REGISTRADAS: {self.get_total_locacao()}"),
            separador,
            linha("DESENVOLVIDO POR ALUNOS"),
        ]

        for criador in self.created_by.splitlines():
            linhas.append(linha(criador.strip()))

        linhas.extend([
            separador,
            linha(f"DISCIPLINA: {self.disciplina}"),
            linha(f"SEMESTRE: {self.semestre}"),
            borda,
        ])

        return "\n".join(linhas)
