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


    def _exibir_relatorio(self, titulo: str, dados):
        """Padroniza a apresentação dos relatórios no terminal."""
        largura = 68
        borda = "=" * largura

        print(f"\n{borda}")
        print(titulo.center(largura))
        print(borda)
        print(dados.to_string(index=False))
        print(borda)
        input("\nPressione Enter para voltar ao menu de relatórios...")

    def get_relatorio_carros(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dados = oracle.sqlToDataFrame(self.query_relatorio_carros)
        self._exibir_relatorio("RELATÓRIO DE CARROS", dados)

    def get_relatorio_locacao_por_carro(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dados = oracle.sqlToDataFrame(self.query_relatorio_locacao_por_carro)
        self._exibir_relatorio("RELATÓRIO DE LOCAÇÕES POR CARRO", dados)

    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dados = oracle.sqlToDataFrame(self.query_relatorio_clientes)
        self._exibir_relatorio("RELATÓRIO DE CLIENTES", dados)

    def get_relatorio_geral(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dados = oracle.sqlToDataFrame(self.query_relatorio_geral)
        self._exibir_relatorio("RELATÓRIO GERAL", dados)
