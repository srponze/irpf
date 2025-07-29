from datetime import date, time


class Movimiento:

    def __init__(
        self,
        fecha: date,
        hora: time,
        producto: str,
        isin: str,
        bolsa: str,
        numero: int,
        precio: float,
        divisa: str,
        valorLocal: float,
        valor: float,
        tipoDeCambio: float,
        comision: float,
        total: float,
    ):
        self.fecha = fecha
        self.hora = hora
        self.producto = producto
        self.isin = isin
        self.bolsa = bolsa
        self.numero = numero
        self.precio = precio
        self.divisa = divisa
        self.valorLocal = valorLocal
        self.valor = valor
        self.tipoDeCambio = tipoDeCambio
        self.comision = comision
        self.total = total

    def indent(self, string, longitudIndent):
        string = str(string)
        longitudIndent += 1
        return (
            string + " " * (longitudIndent - len(string))
            if len(string) < longitudIndent
            else ""
        )

    def __str__(self):
        i = self.indent
        return (
            f"{self.fecha} {self.hora} {i(self.producto[0:21],21)}"
            f"{i(self.isin,12)} {i(self.numero,6)} {i(round(self.precio, 4), 8)}"
            f"{self.divisa} {i(round(self.valorLocal, 2),9)}"
            f"{i(round(self.valor, 2),9)} {i(round(self.tipoDeCambio, 4),6)}"
            f"{i(round(self.comision, 2),7)} {round(self.total, 2)}"
        )
