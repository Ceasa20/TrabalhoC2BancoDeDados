from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_produtos = config.QUERY_COUNT.format(tabela="carros")
        self.qry_total_clientes = config.QUERY_COUNT.format(tabela="clientes")
        self.qry_total_fornecedores = config.QUERY_COUNT.format(tabela="locacao")
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

    def get_total_locacoes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_locacoes)["total_locacoes"].values[0]


    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE VENDAS                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - CARROS:         {str(self.get_total_carros()).rjust(5)}
        #      2 - CLIENTES:         {str(self.get_total_clientes()).rjust(5)}
        #      3 - LOCACOES:     {str(self.get_total_locacoes()).rjust(5)}
        #      
        #
        #  CRIADO POR ALUNOS: {self.created_by}
        #
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """