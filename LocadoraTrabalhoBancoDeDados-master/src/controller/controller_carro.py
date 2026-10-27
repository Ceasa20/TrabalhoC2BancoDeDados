from model.carros import Carros
from conexion.oracle_queries import OracleQueries
from utils import config
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

    def desativar_carro(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        placa = self.solicitar_placa(
            "Placa do carro que deseja desativar: "
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

            print("Carro desativado com sucesso.")
            print(carro_inativado.to_string())
        else:
            print(f"O carro com placa {placa} não existe.")

    def excluir_carro(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        carros = oracle.sqlToDataFrame(
            "select placa, marca, modelo from carros order by placa"
        )
        if carros.empty:
            print("Não há veículos cadastrados para excluir.")
            return

        print("\nVeículos:")
        for indice, (_, carro) in enumerate(carros.iterrows(), start=1):
            print(
                f"[{indice}] Placa: {carro['placa']} | "
                f"{carro['marca']} {carro['modelo']}"
            )

        opcoes = ("0",) + tuple(
            str(indice) for indice in range(1, len(carros) + 1)
        )
        opcao = config.solicitar_opcao(
            "Selecione o veículo que deseja excluir (0 para cancelar): ",
            opcoes
        )
        if opcao == "0":
            return

        placa = carros.iloc[int(opcao) - 1]["placa"]
        confirmar = config.solicitar_opcao(
            f"Confirma a exclusão permanente do veículo {placa}? [S/N]: ",
            ("S", "N")
        )
        if confirmar != "S":
            print("Exclusão cancelada.")
            return

        locacoes = oracle.sqlToDataFrame(
            "select codigo_locacao from locacao where placa = :placa",
            {"placa": placa}
        )
        statements = []
        if not locacoes.empty:
            confirmar_locacoes = config.solicitar_opcao(
                f"Este veículo possui {len(locacoes)} locação(ões). "
                "Deseja excluir também essas locações? [S/N]: ",
                ("S", "N")
            )
            if confirmar_locacoes != "S":
                print(
                    "O veículo não pode ser excluído enquanto houver "
                    "locações vinculadas."
                )
                return

            statements.append((
                "delete from locacao where placa = :placa",
                {"placa": placa}
            ))

        statements.append((
            "delete from carros where placa = :placa",
            {"placa": placa}
        ))
        oracle.write_transaction(statements)
        print(f"Veículo {placa} excluído com sucesso.")

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
