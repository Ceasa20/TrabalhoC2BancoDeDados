from model.clientes import Cliente
from conexion.oracle_queries import OracleQueries

class Controller_Cliente:
    def __init__(self):
        pass

    def solicitar_cpf(self, mensagem: str) -> str:
        while True:
            cpf = input(mensagem).strip()

            if cpf:
                return cpf

            print("O CPF não pode ser vazio.")
        
    def inserir_cliente(self) -> Cliente:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CPF
        cpf = self.solicitar_cpf("CPF (Novo): ")

        if self.verifica_existencia_cliente(oracle, cpf):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Solicita ao usuario o novo telefone
            telefone = input("Telefone (Novo): ")
            # Insere e persiste o novo cliente
            oracle.write(
                "insert into clientes (cpf, nome, telefone, ativo) "
                "values (:cpf, :nome, :telefone, 'S')",
                {"cpf": cpf, "nome": nome, "telefone": telefone}
            )
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(
                "select cpf, nome, telefone, ativo from clientes where cpf = :cpf",
                {"cpf": cpf}
            )
            # Cria um novo objeto Cliente
            novo_cliente = Cliente(
                df_cliente.cpf.values[0],
                df_cliente.nome.values[0],
                df_cliente.telefone.values[0],
                df_cliente.ativo.values[0]
            )
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = self.solicitar_cpf("CPF do cliente que deseja alterar o nome: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            # Solicita a nova descrição do cliente
            novo_telefone = input("Telefone (Novo): ")
            ativo = input("Cliente ativo? [S/N]: ").strip().upper()
            while ativo not in ("S", "N"):
                ativo = input("Opção inválida. Informe S ou N: ").strip().upper()
            # Atualiza os dados do cliente existente
            oracle.write(
                "update clientes set nome = :nome, telefone = :telefone, "
                "ativo = :ativo where cpf = :cpf",
                {
                    "nome": novo_nome,
                    "telefone": novo_telefone,
                    "ativo": ativo,
                    "cpf": cpf
                }
            )
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(
                "select cpf, nome, telefone, ativo from clientes where cpf = :cpf",
                {"cpf": cpf}
            )
            # Cria um novo objeto cliente
            cliente_atualizado = Cliente(
                df_cliente.cpf.values[0],
                df_cliente.nome.values[0],
                df_cliente.telefone.values[0],
                df_cliente.ativo.values[0]
            )
            # Exibe os atributos do novo cliente
            print(cliente_atualizado.to_string())
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return cliente_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF do Cliente a ser inativado
        cpf = self.solicitar_cpf("CPF do cliente que deseja inativar: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(
                "select cpf, nome, telefone, ativo from clientes where cpf = :cpf",
                {"cpf": cpf}
            )
            oracle.write(
                "update clientes set ativo = 'N' where cpf = :cpf",
                {"cpf": cpf}
            )
            cliente_inativado = Cliente(
                df_cliente.cpf.values[0],
                df_cliente.nome.values[0],
                df_cliente.telefone.values[0],
                "N"
            )
            print("Cliente inativado com sucesso.")
            print(cliente_inativado.to_string())
        else:
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_cliente(self, oracle:OracleQueries, cpf:str=None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = oracle.sqlToDataFrame(
            "select cpf, nome, telefone, ativo from clientes where cpf = :cpf",
            {"cpf": cpf}
        )
        return df_cliente.empty
