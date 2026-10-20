from datetime import date
from model.clientes import Cliente
from model.carros import Carros

class Pedido:
    def __init__(self, 
                 codigo_locacao:int=None,
                 cliente:Cliente= None,
                 data_inicio:date=None,
                 data_previsao:date=None,
                 data_fim:date=None,
                 dias:int=None,
                 carros:Carros=None,
                 valor_total:float=None
                 ):
        self.set_codigo_locacao(codigo_locacao)
        self.set_cliente(cliente)
        self.set_data_inicio(data_inicio)
        self.set_data_previsao(data_previsao)
        self.set_data_fim(data_fim)
        self.set_dias(dias)
        self.set_carros(carros)
        self.set_valor_total(valor_total)


def set_codigo_locacao(self, codigo_locacao: int):
    self.codigo_locacao = codigo_locacao

def set_cliente(self, cliente: Cliente):
    self.cliente = cliente

def set_data_inicio(self, data_inicio: date):
    self.data_inicio = data_inicio

def set_data_previsao(self, data_previsao: date):
    self.data_previsao = data_previsao

def set_data_fim(self, data_fim: date):
    self.data_fim = data_fim

def set_dias(self, dias: int):
    self.dias = dias

def set_carros(self, carros: Carros):
    self.carros = carros

def set_valor_total(self, valor_total: float):
    self.valor_total = valor_total


def get_codigo_locacao(self) -> int:
    return self.codigo_locacao

def get_cliente(self) -> Cliente:
    return self.cliente

def get_data_inicio(self) -> date:
    return self.data_inicio

def get_data_previsao(self) -> date:
    return self.data_previsao

def get_data_fim(self) -> date:
    return self.data_fim

def get_dias(self) -> int:
    return self.dias

def get_carros(self) -> Carros:
    return self.carros

def get_valor_total(self) -> float:
    return self.valor_total


def to_string(self) -> str:
    return f"Locação: {self.get_codigo_locacao()} | Cliente: {self.get_cliente().get_nome()} | Data Início: {self.get_data_inicio()} | Data Previsão: {self.get_data_previsao()} | Data Fim: {self.get_data_fim()} | Dias: {self.get_dias()} | Carro: {self.get_carros().get_modelo()} | Valor Total: {self.get_valor_total()}"