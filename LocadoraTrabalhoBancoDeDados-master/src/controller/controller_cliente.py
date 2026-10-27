
from model.clientes import Cliente
from conexion.oracle_queries import OracleQueries
from utils import config
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

    def desativar_cliente(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = self.solicitar_cpf(
            "CPF do cliente que deseja desativar (0 para voltar): "
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

            print("Cliente desativado com sucesso.")
            print(cliente_inativado.to_string())

        else:
            print(f"O CPF {cpf} não existe.")

    def excluir_cliente(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        clientes = oracle.sqlToDataFrame(
            "select cpf, nome from clientes order by nome"
        )
        if clientes.empty:
            print("Não há clientes cadastrados para excluir.")
            return

        print("\nClientes:")
        for indice, (_, cliente) in enumerate(clientes.iterrows(), start=1):
            print(f"[{indice}] CPF: {cliente['cpf']} | Nome: {cliente['nome']}")

        opcoes = ("0",) + tuple(
            str(indice) for indice in range(1, len(clientes) + 1)
        )
        opcao = config.solicitar_opcao(
            "Selecione o cliente que deseja excluir (0 para cancelar): ",
            opcoes
        )
        if opcao == "0":
            return

        cpf = clientes.iloc[int(opcao) - 1]["cpf"]
        confirmar = config.solicitar_opcao(
            f"Confirma a exclusão permanente do cliente {cpf}? [S/N]: ",
            ("S", "N")
        )
        if confirmar != "S":
            print("Exclusão cancelada.")
            return

        locacoes = oracle.sqlToDataFrame(
            "select codigo_locacao from locacao where cpf = :cpf",
            {"cpf": cpf}
        )
        statements = []
        if not locacoes.empty:
            confirmar_locacoes = config.solicitar_opcao(
                f"Este cliente possui {len(locacoes)} locação(ões). "
                "Deseja excluir também essas locações? [S/N]: ",
                ("S", "N")
            )
            if confirmar_locacoes != "S":
                print(
                    "O cliente não pode ser excluído enquanto houver "
                    "locações vinculadas."
                )
                return

            statements.append((
                "delete from locacao where cpf = :cpf",
                {"cpf": cpf}
            ))

        statements.append((
            "delete from clientes where cpf = :cpf",
            {"cpf": cpf}
        ))
        oracle.write_transaction(statements)
        print(f"Cliente {cpf} excluído com sucesso.")

    def verifica_existencia_cliente(
        self, oracle: OracleQueries, cpf: str = None
    ) -> bool:
        df_cliente = oracle.sqlToDataFrame(
            "select cpf, nome, telefone, ativo "
            "from clientes where cpf = :cpf",
            {"cpf": cpf}
        )
        return df_cliente.empty
