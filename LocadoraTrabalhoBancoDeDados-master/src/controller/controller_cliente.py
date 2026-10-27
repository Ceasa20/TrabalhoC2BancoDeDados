
from model.clientes import Cliente
from conexion.oracle_queries import OracleQueries
import os


def input_ou_voltar(mensagem):
    valor = input(mensagem).strip()

    if valor == "0":
        os.system("clear")
        print("\nVoltando ao menu anterior...")
        return None

    return valor


class Controller_Cliente:

    def __init__(self):
        pass

    def solicitar_cpf(self, mensagem: str) -> str:
        while True:
            cpf = input_ou_voltar(mensagem)

            if cpf is None:
                return None

            if cpf:
                return cpf

            print("O CPF não pode ser vazio.")

    def inserir_cliente(self) -> Cliente:
        os.system("clear")
        print("\n=== CADASTRO DE CLIENTE ===")
        print("Digite 0 em qualquer campo para voltar.")

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = self.solicitar_cpf("CPF (Novo): ")

        if cpf is None:
            return None

        if self.verifica_existencia_cliente(oracle, cpf):
            nome = input_ou_voltar("Nome (Novo): ")

            if nome is None:
                return None

            telefone = input_ou_voltar("Telefone (Novo): ")

            if telefone is None:
                return None

            oracle.write(
                "insert into clientes (cpf, nome, telefone, ativo) "
                "values (:cpf, :nome, :telefone, 'S')",
                {"cpf": cpf, "nome": nome, "telefone": telefone}
            )

            df_cliente = oracle.sqlToDataFrame(
                "select cpf, nome, telefone, ativo "
                "from clientes where cpf = :cpf",
                {"cpf": cpf}
            )

            novo_cliente = Cliente(
                df_cliente.cpf.values[0],
                df_cliente.nome.values[0],
                df_cliente.telefone.values[0],
                df_cliente.ativo.values[0]
            )

            print(novo_cliente.to_string())
            return novo_cliente

        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = self.solicitar_cpf(
            "CPF do cliente que deseja alterar (0 para voltar): "
        )

        if cpf is None:
            return None

        if not self.verifica_existencia_cliente(oracle, cpf):
            novo_nome = input_ou_voltar("Nome (Novo) (0 para voltar): ")
            if novo_nome is None:
                return None

            novo_telefone = input_ou_voltar(
                "Telefone (Novo) (0 para voltar): "
            )
            if novo_telefone is None:
                return None

            ativo = input_ou_voltar("Cliente ativo? [S/N] (0 para voltar): ")

            if ativo is None:
                return None

            ativo = ativo.upper()

            while ativo not in ("S", "N"):
                ativo = input_ou_voltar(
                    "Opção inválida. Informe S ou N (0 para voltar): "
                )

                if ativo is None:
                    return None

                ativo = ativo.upper()

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

            df_cliente = oracle.sqlToDataFrame(
                "select cpf, nome, telefone, ativo "
                "from clientes where cpf = :cpf",
                {"cpf": cpf}
            )

            cliente_atualizado = Cliente(
                df_cliente.cpf.values[0],
                df_cliente.nome.values[0],
                df_cliente.telefone.values[0],
                df_cliente.ativo.values[0]
            )

            print(cliente_atualizado.to_string())
            return cliente_atualizado

        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_cliente(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = self.solicitar_cpf(
            "CPF do cliente que deseja inativar (0 para voltar): "
        )

        if cpf is None:
            return

        if not self.verifica_existencia_cliente(oracle, cpf):
            df_cliente = oracle.sqlToDataFrame(
                "select cpf, nome, telefone, ativo "
                "from clientes where cpf = :cpf",
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

    def verifica_existencia_cliente(
        self, oracle: OracleQueries, cpf: str = None
    ) -> bool:
        df_cliente = oracle.sqlToDataFrame(
            "select cpf, nome, telefone, ativo "
            "from clientes where cpf = :cpf",
            {"cpf": cpf}
        )
        return df_cliente.empty
