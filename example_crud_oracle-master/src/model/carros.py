class Carros:
    def __init__(self, 
                 placa:str=None,
                 marca:str=None,
                 modelo:str=None,
                 valorDiaria:float=0 
                 ):
        self.set_placa(placa)
        self.set_marca(marca)
        self.set_modelo(modelo)
        self.set_valor_diaria(valorDiaria)

    def set_placa(self, placa:str):
        self.placa = placa

    def set_marca(self, marca:str):
        self.marca = marca

    def set_modelo(self, modelo:str):
        self.modelo = modelo

    def set_valorDiaria(self, valorDiaria:str):
        self.valorDiaria = valorDiaria

    def get_placa(self) -> str:
        return self.placa

    def get_marca(self) -> str:
        return self.marca

    def get_modelo(self) -> str:
        return self.modelo

    def get_valorDiaria(self) -> str:
        return self.valorDiaria



    def to_string(self) -> str:
        return f"Código: {self.get_codigo()} | Placa: {self.get_placa()} | Marca: {self.get_marca()} | Modelo: {self.get_modelo()} | Valor Diária: {self.get_valorDiaria()}"