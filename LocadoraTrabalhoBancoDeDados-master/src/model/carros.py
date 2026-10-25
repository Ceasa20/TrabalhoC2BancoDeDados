class Carros:
    def __init__(self, 
                 placa:str=None,
                 marca:str=None,
                 modelo:str=None,
                 valorDiaria:float=0,
                 ativo:str="S"
                 ):
        self.set_placa(placa)
        self.set_marca(marca)
        self.set_modelo(modelo)
        self.set_valor_diaria(valorDiaria)
        self.set_ativo(ativo)

    def set_placa(self, placa:str):
        self.placa = placa

    def set_marca(self, marca:str):
        self.marca = marca

    def set_modelo(self, modelo:str):
        self.modelo = modelo

    def set_valor_diaria(self, valor_diaria:float):
        self.valor_diaria = valor_diaria

    def set_ativo(self, ativo:str):
        self.ativo = ativo

    def get_placa(self) -> str:
        return self.placa

    def get_marca(self) -> str:
        return self.marca

    def get_modelo(self) -> str:
        return self.modelo

    def get_valor_diaria(self) -> float:
        return self.valor_diaria

    def get_ativo(self) -> str:
        return self.ativo



    def to_string(self) -> str:
        return f"Placa: {self.get_placa()} | Marca: {self.get_marca()} | Modelo: {self.get_modelo()} | Valor Diária: {self.get_valor_diaria()} | Ativo: {self.get_ativo()}"