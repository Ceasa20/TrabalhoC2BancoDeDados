
###########################################################################
# Author: Howard Roatti
# Created: 02/09/2022
# Last Update: 03/09/2022
#
# Essa classe auxilia na conexão com o Banco de Dados Oracle
###########################################################################
import json
from pathlib import Path

import cx_Oracle
from pandas import DataFrame


class OracleQueries:

    def __init__(self, can_write: bool = False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = "XEPDB1"
        self.sid = "XE"

        # Inicializa os atributos para evitar erros se a conexão falhar.
        self.conn = None
        self.cur = None

        credentials_path = (
            Path(__file__).resolve().parent
            / "passphrase"
            / "authentication.oracle"
        )

        with credentials_path.open(encoding="utf-8") as f:
            self.user, self.passwd = f.read().strip().split(",", 1)

        self.user = self.user.strip()
        self.passwd = self.passwd.strip()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def connectionString(self, in_container: bool = False):
        """
        Cria a string de conexão com o banco Oracle.
        """
        if in_container:
            return cx_Oracle.makedsn(
                host=self.host,
                port=self.port,
                service_name=self.service_name
            )

        return cx_Oracle.makedsn(
            host=self.host,
            port=self.port,
            sid=self.sid
        )

    def connect(self):
        self.conn = cx_Oracle.connect(
            user=self.user,
            password=self.passwd,
            dsn=self.connectionString(in_container=True)
        )
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query: str, params: dict = None) -> DataFrame:
        """
        Executa uma consulta e retorna um DataFrame.
        """
        self.cur.execute(query, params or {})
        rows = self.cur.fetchall()
        columns = [col[0].lower() for col in self.cur.description]
        return DataFrame(rows, columns=columns)

    def sqlToMatrix(self, query: str) -> tuple:
        """
        Executa uma consulta e retorna uma matriz e os nomes das colunas.
        """
        self.cur.execute(query)
        rows = self.cur.fetchall()
        matrix = [list(row) for row in rows]
        columns = [col[0].lower() for col in self.cur.description]
        return matrix, columns

    def sqlToJson(self, query: str):
        """
        Executa uma consulta e retorna os resultados em JSON.
        """
        self.cur.execute(query)
        columns = [col[0].lower() for col in self.cur.description]
        self.cur.rowfactory = lambda *args: dict(zip(columns, args))
        rows = self.cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query: str, params: dict = None):
        if not self.can_write:
            raise Exception("Can't write using this connection")

        self.cur.execute(query, params or {})
        self.conn.commit()

    def close(self):
        if self.cur is not None:
            self.cur.close()
            self.cur = None

        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def executeDDL(self, query: str):
        """
        Executa um comando DDL.
        """
        self.cur.execute(query)
