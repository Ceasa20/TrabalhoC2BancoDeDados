from model.carros import Carros
from conexion.oracle_queries import OracleQueries
import math

class Controller_Carro:
    def __init__(self):
        pass
        
    def inserir_carro(self) -> Carros:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario a nova placa
        placa = input("Placa (Nova): ")

        if self.verifica_existencia_carro(oracle, placa):
            # Solicita ao usuario a nova marca
            marca = input("Marca (Nova): ")
            # Solicita ao usuario o novo modelo
            modelo = input("Modelo (Novo): ")
            # Solicita ao usuario o novo valor da diária
            valor_diaria = self.solicitar_valor_diaria()

            # Insere e persiste o novo carro
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
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(
                "select placa, marca, modelo, valor_diaria, ativo "
                "from carros where placa = :placa",
                {"placa": placa}
            )
            # Cria um novo objeto carro
            novo_carro = Carros(
                df_carro.placa.values[0],
                df_carro.marca.values[0],
                df_carro.modelo.values[0],
                df_carro.valor_diaria.values[0],
                df_carro.ativo.values[0]
            )
            # Exibe os atributos do novo carro
            print(novo_carro.to_string())
            # Retorna o objeto novo_carro para utilização posterior, caso necessário
            return novo_carro
        else:
            print(f"O carro com placa {placa} já está cadastrado.")
            return None

    def atualizar_carro(self) -> Carros:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do carro a ser alterado
        placa = input("Placa do carro que deseja atualizar: ")

        # Verifica se o carro existe na base de dados
        if not self.verifica_existencia_carro(oracle, placa):
            # Solicita ao usuario a nova marca
            marca = input("Marca (Nova): ")
            # Solicita ao usuario o novo modelo
            modelo = input("Modelo (Novo): ")
            # Solicita ao usuario o novo valor da diária
            valor_diaria = self.solicitar_valor_diaria()
            ativo = input("Carro ativo? [S/N]: ").strip().upper()
            while ativo not in ("S", "N"):
                ativo = input("Opção inválida. Informe S ou N: ").strip().upper()
            # Atualiza os dados do carro existente
            oracle.write(
                "update carros set marca = :marca, modelo = :modelo, "
                "valor_diaria = :valor_diaria, ativo = :ativo where placa = :placa",
                {
                    "marca": marca,
                    "modelo": modelo,
                    "valor_diaria": valor_diaria,
                    "ativo": ativo,
                    "placa": placa
                }
            )
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(
                "select placa, marca, modelo, valor_diaria, ativo "
                "from carros where placa = :placa",
                {"placa": placa}
            )
            # Cria um novo objeto carro
            carro_atualizado = Carros(
                df_carro.placa.values[0],
                df_carro.marca.values[0],
                df_carro.modelo.values[0],
                df_carro.valor_diaria.values[0],
                df_carro.ativo.values[0]
            )
            # Exibe os atributos do novo carro
            print(carro_atualizado.to_string())
            # Retorna o objeto carro_atualizado para utilização posterior, caso necessário
            return carro_atualizado
        else:
            print(f"O carro com placa {placa} não existe.")
            return None

    def excluir_carro(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o carro a ser excluído
        placa = input("Placa do carro que irá excluir: ")

        # Verifica se o carro existe na base de dados
        if not self.verifica_existencia_carro(oracle, placa):
            # Recupera os dados do novo carro criado transformando em um DataFrame
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

    def verifica_existencia_carro(self, oracle:OracleQueries, placa:str=None) -> bool:
        # Recupera os dados do novo carro criado transformando em um DataFrame
        df_carro = oracle.sqlToDataFrame(
            "select placa, marca, modelo, valor_diaria, ativo "
            "from carros where placa = :placa",
            {"placa": placa}
        )
        return df_carro.empty

    def solicitar_valor_diaria(self) -> float:
        while True:
            entrada = input("Valor da Diária (Novo): ").strip().replace(",", ".")
            try:
                valor_diaria = float(entrada)
            except ValueError:
                print("Valor inválido. Informe um número, por exemplo 150.00.")
                continue

            if not math.isfinite(valor_diaria) or valor_diaria <= 0:
                print("A diária deve ser um valor positivo.")
                continue

            return valor_diaria