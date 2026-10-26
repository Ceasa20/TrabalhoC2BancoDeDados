from pydoc import cli
from model.carros import Carros
from controller.controller_carro import Controller_Carro
from model.clientes import Cliente
from controller.controller_cliente import Controller_Cliente
from model.locacao import Locacao
from conexion.oracle_queries import OracleQueries
from datetime import date

class Controller_Locacao:
    def __init__(self):
        self.ctrl_cliente = Controller_Cliente()
        self.ctrl_carros = Controller_Carro()
        
    def inserir_locacao(self) -> Locacao:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista os clientes existentes para inserir na locacao
        self.listar_clientes(oracle, need_connect=True)
        cpf = str(input("Digite o número do CPF do Cliente: "))
        cliente = self.valida_cliente(oracle, cpf)
        if cliente == None:
            return None

        # Lista os carros existentes para inserir na locacao
        self.listar_carros(oracle, need_connect=True)
        placa = self.solicitar_placa("Digite a placa do Carro: ")
        carro = self.valida_carro(oracle, placa)
        if carro == None:
            return None

        # Perguntar ao usuario até quando ele deseja alugar o carro, e calcular a quantidade de dias
        data_previsao_locacao = self.solicitar_data_previsao()
        dias_locacao = (data_previsao_locacao - date.today()).days

        data_hoje = date.today()

        #calcular valor total da locacao
        valor_total = carro.get_valor_diaria() * dias_locacao

        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, data_inicio_locacao=data_hoje, data_previsao_locacao=data_previsao_locacao, cpf=cliente.get_CPF(), placa=carro.get_placa(), dias_locacao=dias_locacao, valor_total=valor_total)
        # Executa o bloco PL/SQL anônimo para inserção da nova locacao e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := LOCACAO_CODIGO_LOCACAO_SEQ.NEXTVAL;
            insert into locacao values(:codigo, :data_inicio_locacao, :data_previsao_locacao, NULL, :dias_locacao, :valor_total, :cpf, :placa);
        end;
        """, data)
        # Recupera o código da nova locação
        codigo_locacao = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados da nova locação criada transformando em um DataFrame
        df_locacao = oracle.sqlToDataFrame(
            "select codigo_locacao, data_inicio_locacao, dias_locacao, valor_total "
            "from locacao where codigo_locacao = :codigo_locacao",
            {"codigo_locacao": codigo_locacao}
        )
        # Cria um novo objeto Locacao
        nova_locacao = Locacao(
            codigo_locacao=df_locacao.codigo_locacao.values[0],
            cliente=cliente,
            data_inicio=df_locacao.data_inicio_locacao.values[0],
            data_previsao=data_previsao_locacao,
            data_fim=None,
            dias=df_locacao.dias_locacao.values[0],
            carros=carro,
            valor_total=df_locacao.valor_total.values[0]
        )
        # Exibe os atributos da nova locação
        print(nova_locacao.to_string())
        # Retorna o objeto nova_locacao para utilização posterior, caso necessário
        return nova_locacao

    def atualizar_locacao(self) -> Locacao:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da locação a ser alterada
        self.listar_locacoes(oracle)
        codigo_locacao = self.solicitar_codigo_locacao(
            "Código da Locação que irá alterar: "
        )

        # Verifica se a locação existe na base de dados
        if not self.verifica_existencia_locacao(oracle, codigo_locacao):
            df_finalizacao = oracle.sqlToDataFrame(
                "select data_fim_locacao from locacao "
                "where codigo_locacao = :codigo_locacao "
                "and data_fim_locacao is not null",
                {"codigo_locacao": codigo_locacao}
            )
            if not df_finalizacao.empty:
                print(f"A locação {codigo_locacao} já foi finalizada e não pode ser alterada.")
                return None

            self.listar_carros(oracle)
            placa = self.solicitar_placa("Digite a placa do novo carro: ")
            carro = self.valida_carro(oracle, placa)
            if carro is None:
                return None

            oracle.write(
                "update locacao "
                "set placa = :placa, "
                "valor_total = dias_locacao * :valor_diaria "
                "where codigo_locacao = :codigo_locacao",
                {
                    "placa": carro.get_placa(),
                    "valor_diaria": carro.get_valor_diaria(),
                    "codigo_locacao": codigo_locacao
                }
            )
            print(f"Carro da locação {codigo_locacao} atualizado para {carro.get_modelo()}.")
            return None
        else:
            print(f"O código {codigo_locacao} não existe.")
            return None

    def finalizar_locacao(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        self.listar_locacoes(oracle)
        codigo_locacao = self.solicitar_codigo_locacao(
            "Código da Locação que deseja finalizar: "
        )

        if self.verifica_existencia_locacao(oracle, codigo_locacao):
            print(f"O código {codigo_locacao} não existe.")
            return

        df_finalizacao = oracle.sqlToDataFrame(
            "select data_fim_locacao from locacao "
            "where codigo_locacao = :codigo_locacao "
            "and data_fim_locacao is not null",
            {"codigo_locacao": codigo_locacao}
        )
        if not df_finalizacao.empty:
            print(f"A locação {codigo_locacao} já foi finalizada.")
            return

        confirmar = input(
            f"Confirma a finalização da locação {codigo_locacao}? [S/N]: "
        ).strip().upper()
        if confirmar != "S":
            print("Finalização cancelada.")
            return

        oracle.write(
            "update locacao set data_fim_locacao = :data_fim "
            "where codigo_locacao = :codigo_locacao "
            "and data_fim_locacao is null",
            {
                "data_fim": date.today(),
                "codigo_locacao": codigo_locacao
            }
        )
        print(f"Locação {codigo_locacao} finalizada em {date.today():%d/%m/%Y}.")

    def verifica_existencia_locacao(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados da nova locação criada transformando em um DataFrame
        df_locacao = oracle.sqlToDataFrame(
            "select codigo_locacao, data_inicio_locacao "
            "from locacao where codigo_locacao = :codigo",
            {"codigo": codigo}
        )
        return df_locacao.empty

    def solicitar_codigo_locacao(self, prompt: str) -> int:
        while True:
            entrada = input(prompt).strip()
            try:
                codigo_locacao = int(entrada)
            except ValueError:
                print("Código inválido. Informe um número inteiro.")
                continue

            if codigo_locacao <= 0:
                print("O código da locação deve ser maior que zero.")
                continue

            return codigo_locacao

    def solicitar_placa(self, mensagem: str) -> str:
        while True:
            placa = input(mensagem).strip().upper()

            if placa:
                return placa

            print("A placa não pode ser vazia.")

    def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.cpf
                    , c.nome 
                from clientes c
                where c.ativo = 'S'
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_locacoes(self, oracle: OracleQueries, need_connect: bool = False):
        query = """
                select l.codigo_locacao
                    , c.nome as cliente_nome
                    , ca.placa
                    , ca.modelo as carro_modelo
                    , l.data_fim_locacao
                from locacao l
                inner join clientes c on l.cpf = c.cpf
                inner join carros ca on l.placa = ca.placa
                order by l.codigo_locacao
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))


    def listar_carros(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.placa
                    , c.modelo
                    , c.marca
                    , c.valor_diaria
                from carros c
                where c.ativo = 'S'
                order by c.modelo
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_cliente(self, oracle:OracleQueries, cpf:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(oracle, cpf):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(
                "select cpf, nome, ativo from clientes "
                "where cpf = :cpf",
                {"cpf": cpf}
            )
            if df_cliente.ativo.values[0].strip().upper() != "S":
                print(f"O cliente com CPF {cpf} está inativo e não pode alugar.")
                return None
            # Cria um novo objeto cliente
            cliente = Cliente(
                df_cliente.cpf.values[0],
                df_cliente.nome.values[0],
                ativo=df_cliente.ativo.values[0]
            )
            return cliente

    def valida_carro(
        self,
        oracle: OracleQueries,
        placa: str = None,
        exigir_ativo: bool = True
    ) -> Carros:
        if self.ctrl_carros.verifica_existencia_carro(oracle, placa):
            print(f"A placa {placa} informada não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(
                "select placa, marca, modelo, valor_diaria, ativo "
                "from carros where placa = :placa",
                {"placa": placa}
            )
            # Cria um novo objeto carro
            carro = Carros(
                df_carro.placa.values[0],
                df_carro.marca.values[0],
                df_carro.modelo.values[0],
                df_carro.valor_diaria.values[0],
                df_carro.ativo.values[0]
            )
            if exigir_ativo and df_carro.ativo.values[0].strip().upper() != "S":
                print(f"O carro com placa {placa} está inativo e não pode ser alugado.")
                return None
            return carro

    def solicitar_data_previsao(self) -> date:
        while True:
            entrada = input(
                "Digite a data prevista para devolução (YYYY-MM-DD): "
            ).strip()

            try:
                data_previsao = date.fromisoformat(entrada)
            except ValueError:
                print("Data inválida. Use o formato YYYY-MM-DD.")
                continue

            if data_previsao <= date.today():
                print("A data prevista deve ser posterior à data de hoje.")
                continue

            return data_previsao

        
