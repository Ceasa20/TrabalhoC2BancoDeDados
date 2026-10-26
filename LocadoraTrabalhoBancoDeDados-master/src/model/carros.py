
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
        if placa is not None and placa.strip():
            self.placa = placa.strip().upper()
        else:
            raise ValueError("A placa não pode ser vazia.")

    def set_marca(self, marca:str):
        if marca is not None and marca.strip():
            self.marca = marca.strip()
        else:
            raise ValueError("A marca não pode ser vazia.")

    def set_modelo(self, modelo:str):
        if modelo is not None and modelo.strip():
            self.modelo = modelo.strip()
        else:
            raise ValueError("O modelo não pode ser vazio.")

    def set_valor_diaria(self, valor_diaria:float):
        if valor_diaria < 0:
            raise ValueError("O valor da diária não pode ser negativo.")
        self.valor_diaria = valor_diaria

    def set_ativo(self, ativo:str):
        ativo = ativo.upper()
        if ativo not in ("S", "N"):
            raise ValueError("O status deve ser S ou N.")
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
