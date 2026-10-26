
from pathlib import Path

from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        sql_dir = Path(__file__).resolve().parent.parent / "sql"

        # Abre o arquivo com a consulta e associa a um atributo da classe
        with (sql_dir / "relatorio_carros.sql").open(encoding="utf-8") as f:
            self.query_relatorio_carros = f.read()

        # Abre o arquivo com a consulta e associa a um atributo da classe
        with (sql_dir / "relatorio_clientes.sql").open(encoding="utf-8") as f:
            self.query_relatorio_clientes = f.read()

        # Abre o arquivo com a consulta e associa a um atributo da classe
        with (sql_dir / "relatorio_locacao_por_carro.sql").open(encoding="utf-8") as f:
            self.query_relatorio_locacao_por_carro = f.read()

        # Abre o arquivo com a consulta e associa a um atributo da classe
        with (sql_dir / "relatorio_geral.sql").open(encoding="utf-8") as f:
            self.query_relatorio_geral = f.read()


    def get_relatorio_carros(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n" + "=" * 68)
        print("RELATÓRIO DE CARROS".center(68))
        print("=" * 68)
        print(oracle.sqlToDataFrame(self.query_relatorio_carros).to_string(index=False))
        print("=" * 68)
        input("Pressione Enter para Sair do Relatório de Carros")

    def get_relatorio_locacao_por_carro(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n" + "=" * 68)
        print("RELATÓRIO DE LOCAÇÕES POR CARRO".center(68))
        print("=" * 68)
        print(oracle.sqlToDataFrame(self.query_relatorio_locacao_por_carro).to_string(index=False))
        print("=" * 68)
        input("Pressione Enter para Sair do Relatório de Locações por Carro")

    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n" + "=" * 68)
        print("RELATÓRIO DE CLIENTES".center(68))
        print("=" * 68)
        print(oracle.sqlToDataFrame(self.query_relatorio_clientes).to_string(index=False))
        print("=" * 68)
        input("Pressione Enter para Sair do Relatório de Clientes")

    def get_relatorio_geral(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print("\n" + "=" * 68)
        print("RELATÓRIO GERAL".center(68))
        print("=" * 68)
        print(oracle.sqlToDataFrame(self.query_relatorio_geral).to_string(index=False))
        print("=" * 68)
        input("Pressione Enter para Sair do Relatório Geral")
