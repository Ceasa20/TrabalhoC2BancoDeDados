from pydoc import cli
from model.carros import Carros
from controller.controller_carro import Controller_Carro
from model.clientes import Cliente
from controller.controller_cliente import Controller_Cliente
from model.locacao import Locacao
from controller.controller_locacao import Controller_Locacao
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
        placa = str(input("Digite a placa do Carro: "))
        carro = self.valida_carro(oracle, placa)
        if carro == None:
            return None

        data_hoje = date.today()

        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, data_locacao=data_hoje, cpf=cliente.get_CPF(), placa=carro.get_Placa())
        # Executa o bloco PL/SQL anônimo para inserção da nova locacao e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := LOCACOES_CODIGO_LOCACAO_SEQ.NEXTVAL;
            insert into locacoes values(:codigo, :data_locacao, :cpf, :placa);
        end;
        """, data)
        # Recupera o código da nova locação
        codigo_locacao = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados da nova locação criada transformando em um DataFrame
        df_locacao = oracle.sqlToDataFrame(f"select codigo_locacao, data_locacao from locacoes where codigo_locacao = {codigo_locacao}")
        # Cria um novo objeto Locacao
        nova_locacao = Locacao(df_locacao.codigo_locacao.values[0], df_locacao.data_locacao.values[0], cliente, carro)
        # Exibe os atributos da nova locação
        print(nova_locacao.to_string())
        # Retorna o objeto nova_locacao para utilização posterior, caso necessário
        return nova_locacao

    def atualizar_locacao(self) -> Locacao:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da locação a ser alterada
        codigo_locacao = int(input("Código da Locação que irá alterar: "))        

        # Verifica se a locação existe na base de dados
        if not self.verifica_existencia_locacao(oracle, codigo_locacao):

            # Lista os clientes existentes para inserir na locação
            self.listar_clientes(oracle)
            cpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(oracle, cpf)
            if cliente == None:
                return None

            # Lista os carros existentes para inserir na locação
            self.listar_carros(oracle)
            placa = str(input("Digite a placa do Carro: "))
            carro = self.valida_carro(oracle, placa)
            if carro == None:
                return None

            data_hoje = date.today()

            # Atualiza a descrição da locacao existente
            oracle.write(f"update locacoes set cpf = '{cliente.get_CPF()}', placa = '{carro.get_Placa()}', data_locacao = to_date('{data_hoje}','yyyy-mm-dd') where codigo_locacao = {codigo_locacao}")
            # Recupera os dados da nova locação criada transformando em um DataFrame
            df_locacao = oracle.sqlToDataFrame(f"select codigo_locacao, data_locacao from locacoes where codigo_locacao = {codigo_locacao}")
            # Cria um novo objeto Locacao
            locacao_atualizada = Locacao(df_locacao.codigo_locacao.values[0], df_locacao.data_locacao.values[0], cliente, carro)
            # Exibe os atributos da nova locação
            print(locacao_atualizada.to_string())
            # Retorna o objeto locacao_atualizada para utilização posterior, caso necessário
            return locacao_atualizada
        else:
            print(f"O código {codigo_locacao} não existe.")
            return None

    def excluir_locacao(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da locação a ser excluída
        codigo_locacao = int(input("Código da Locação que irá excluir: "))        

        # Verifica se a locação existe na base de dados
        if not self.verifica_existencia_locacao(oracle, codigo_locacao):            
            # Recupera os dados da nova locação criada transformando em um DataFrame
            df_locacao = oracle.sqlToDataFrame(f"select codigo_locacao, data_locacao, cpf, placa from locacoes where codigo_locacao = {codigo_locacao}")
            cliente = self.valida_cliente(oracle, df_locacao.cpf.values[0])
            carro = self.valida_carro(oracle, df_locacao.placa.values[0])

            opcao_excluir = input(f"Tem certeza que deseja excluir a locação {codigo_locacao} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso a locação possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir a locação {codigo_locacao} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    oracle.write(f"delete from itens_locacao where codigo_locacao = {codigo_locacao}")
                    print("Itens da locação removidos com sucesso!")
                    oracle.write(f"delete from locacoes where codigo_locacao = {codigo_locacao}")
                    # Cria um novo objeto Locacao para informar que foi removido
                    locacao_excluida = Locacao(df_locacao.codigo_locacao.values[0], df_locacao.data_locacao.values[0], cliente, carro)
                    # Exibe os atributos da locação excluída
                    print("Locação Removida com Sucesso!")
                    print(locacao_excluida.to_string())
        else:
            print(f"O código {codigo_locacao} não existe.")

    def verifica_existencia_locacao(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados da nova locação criada transformando em um DataFrame
        df_locacao = oracle.sqlToDataFrame(f"select codigo_locacao, data_locacao from locacoes where codigo_locacao = {codigo}")
        return df_locacao.empty

    def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.cpf
                    , c.nome 
                from clientes c
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))


    def listar_carros(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.placa
                    , c.razao_social
                    , c.nome_fantasia
                from carros c
                order by c.nome_fantasia
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
            df_cliente = oracle.sqlToDataFrame(f"select cpf, nome from clientes where cpf = {cpf}")
            # Cria um novo objeto cliente
            cliente = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
            return cliente

    def valida_carro(self, oracle:OracleQueries, placa:str=None) -> Carros:
        if self.ctrl_carro.verifica_existencia_carro(oracle, placa):
            print(f"A placa {placa} informada não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(f"select placa, razao_social, nome_fantasia from carros where placa = {placa}")
            # Cria um novo objeto carro
            carro = Carros(df_carro.placa.values[0], df_carro.razao_social.values[0], df_carro.nome_fantasia.values[0])
            return carro

        