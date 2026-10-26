from model.carros import Carros
from conexion.oracle_queries import OracleQueries
import math

class Controller_Carro:
    def __init__(self):
        pass

    def solicitar_placa(self, mensagem: str) -> str:
        while True:
            placa = input(mensagem).strip().upper()

            if placa:
                return placa

            print("A placa não pode ser vazia.")

    def inserir_carro(self) -> Carros:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        placa = self.solicitar_placa("Placa (Nova): ")

        if self.verifica_existencia_carro(oracle, placa):
            marca = input("Marca (Nova): ")
            modelo = input("Modelo (Novo): ")
            valor_diaria = self.solicitar_valor_diaria()

            oracle.write(
                "insert into carros (placa, modelo, marca, valor_diaria) "
                "values (:placa, :modelo, :marca, :valor_diaria)",
                {
                    "placa": placa,
                    "modelo": modelo,
                    "marca": marca,
                    "valor_diaria": valor_diaria
                }
            )

            df_carro = oracle.sqlToDataFrame(
                "select placa, marca, modelo, valor_diaria, ativo "
                "from carros where placa = :placa",
                {"placa": placa}
            )

            novo_carro = Carros(
                df_carro.placa.values[0],
                df_carro.marca.values[0],
                df_carro.modelo.values[0],
                df_carro.valor_diaria.values[0],
                df_carro.ativo.values[0]
            )

            print(novo_carro.to_string())
            return novo_carro
        else:
            print(f"O carro com placa {placa} já está cadastrado.")
            return None

    def atualizar_carro(self) -> Carros:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        placa = self.solicitar_placa(
            "Placa do carro que deseja atualizar: "
        )

        if not self.verifica_existencia_carro(oracle, placa):
            marca = input("Marca (Nova): ")
            modelo = input("Modelo (Novo): ")
            valor_diaria = self.solicitar_valor_diaria()

            ativo = input("Carro ativo? [S/N]: ").strip().upper()

            while ativo not in ("S", "N"):
                ativo = input(
                    "Opção inválida. Informe S ou N: "
                ).strip().upper()

            oracle.write(
                "update carros set marca = :marca, modelo = :modelo, "
                "valor_diaria = :valor_diaria, ativo = :ativo "
                "where placa = :placa",
                {
                    "marca": marca,
                    "modelo": modelo,
                    "valor_diaria": valor_diaria,
                    "ativo": ativo,
                    "placa": placa
                }
            )

            df_carro = oracle.sqlToDataFrame(
                "select placa, marca, modelo, valor_diaria, ativo "
                "from carros where placa = :placa",
                {"placa": placa}
            )

            carro_atualizado = Carros(
                df_carro.placa.values[0],
                df_carro.marca.values[0],
                df_carro.modelo.values[0],
                df_carro.valor_diaria.values[0],
                df_carro.ativo.values[0]
            )

            print(carro_atualizado.to_string())
            return carro_atualizado
        else:
            print(f"O carro com placa {placa} não existe.")
            return None

    def excluir_carro(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        placa = self.solicitar_placa(
            "Placa do carro que irá excluir: "
        )

        if not self.verifica_existencia_carro(oracle, placa):
            df_carro = oracle.sqlToDataFrame(
                "select placa, marca, modelo, valor_diaria, ativo "
                "from carros where placa = :placa",
                {"placa": placa}
            )

            oracle.write(
                "update carros set ativo = 'N' where placa = :placa",
                {"placa": placa}
            )

            carro_inativado = Carros(
                df_carro.placa.values[0],
                df_carro.marca.values[0],
                df_carro.modelo.values[0],
                df_carro.valor_diaria.values[0],
                "N"
            )

            print("Carro inativado com sucesso.")
            print(carro_inativado.to_string())
        else:
            print(f"O carro com placa {placa} não existe.")

    def verifica_existencia_carro(
        self,
        oracle: OracleQueries,
        placa: str = None
    ) -> bool:
        df_carro = oracle.sqlToDataFrame(
            "select placa, marca, modelo, valor_diaria, ativo "
            "from carros where placa = :placa",
            {"placa": placa}
        )

        return df_carro.empty

    def solicitar_valor_diaria(self) -> float:
        while True:
            entrada = input(
                "Valor da Diária (Novo): "
            ).strip().replace(",", ".")

            try:
                valor_diaria = float(entrada)
            except ValueError:
                print(
                    "Valor inválido. Informe um número, por exemplo 150.00."
                )
                continue

            if not math.isfinite(valor_diaria) or valor_diaria <= 0:
                print("A diária deve ser um valor positivo.")
                continue

            return valor_diaria
