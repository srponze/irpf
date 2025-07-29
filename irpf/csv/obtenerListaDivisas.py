import csv
from typing import List

from irpf.constantes.columnasInformes import *


class ObtenerListaDivisas:

    @staticmethod
    def obtenerListaDivisas(transactionPath):
        divisas: set[str] = set()
        with open(transactionPath, newline="") as csvtransactions:
            reader = csv.reader(csvtransactions)
            for row in reader:
                if row[l(T_DIVISA)] != "":
                    divisas.add(row[l(T_DIVISA)])
        return list(divisas)
