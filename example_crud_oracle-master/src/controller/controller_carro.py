from model.carros import Carros
from conexion.oracle_queries import OracleQueries

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
            # Solicita ao usuario a nova placa
            placa = input("Placa (Nova): ")
            # Solicita ao usuario a nova marca
            marca = input("Marca (Nova): ")
            # Solicita ao usuario o novo modelo
            modelo = input("Modelo (Novo): ")
            # Solicita ao usuario o novo valor da diária
            valorDiaria = input("Valor da Diária (Novo): ")

            # Insere e persiste o novo carro
            oracle.write(f"insert into carros values  ('{placa}', '{marca}', '{modelo}', {valorDiaria})")
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(f"select placa, marca, modelo, valorDiaria from carros where placa = '{placa}'")
            # Cria um novo objeto carro
            novo_carro = Carros(df_carro.placa.values[0], df_carro.marca.values[0], df_carro.modelo.values[0], df_carro.valorDiaria.values[0])
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
            valorDiaria = input("Valor da Diária (Novo): ")
            # Atualiza os dados do carro existente
            oracle.write(f"update carros set marca = '{marca}', modelo = '{modelo}', valorDiaria = {valorDiaria} where placa = '{placa}'")
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(f"select placa, marca, modelo, valorDiaria from carros where placa = '{placa}'")
            # Cria um novo objeto carro
            carro_atualizado = Carros(df_carro.placa.values[0], df_carro.marca.values[0], df_carro.modelo.values[0], df_carro.valorDiaria.values[0])
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
            df_carro = oracle.sqlToDataFrame(f"select placa, marca, modelo, valorDiaria from carros where placa = '{placa}'")
            # Remove o carro da tabela
            oracle.write(f"delete from carros where placa = '{placa}'")
            # Cria um novo objeto carro para informar que foi removido
            carro_excluido = Carros(df_carro.placa.values[0], df_carro.marca.values[0], df_carro.modelo.values[0], df_carro.valorDiaria.values[0])
            # Exibe os atributos do carro excluído
            print("Carro Removido com Sucesso!")
            print(carro_excluido.to_string())
        else:
            print(f"O carro com placa {placa} não existe.")

    def verifica_existencia_carro(self, oracle:OracleQueries, placa:str=None) -> bool:
        # Recupera os dados do novo carro criado transformando em um DataFrame
        df_carro = oracle.sqlToDataFrame(f"select placa, marca, modelo, valorDiaria from carros where placa = '{placa}'")
        return df_carro.empty