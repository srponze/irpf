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

    def __str__(self):
        return (
            f"{self.fecha}  {self.hora}  {self.producto[0:21]:<22} "
            f"{self.isin:<12} {self.numero:7} "
            f"{round(self.precio, 4):10,} {self.divisa} "
            f"{round(self.valorLocal, 2):11,} {self.divisa} "
            f"{round(self.valor, 2):11,} EUR "
            f"{round(self.tipoDeCambio, 4):<6}  "
            f"{round(self.comision, 2):<5} EUR "
            f"{round(self.total, 2):11,} EUR"
        )
