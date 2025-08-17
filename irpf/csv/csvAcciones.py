import csv
from datetime import date, time
from typing import List

from irpf.constantes.columnasInformes import *
from irpf.modelo.movimiento import Movimiento


class CSVAcciones:

    def obtenerAcciones(
        self,
        listaDivisas: List[str],
        transactionPath: str,
        modoDivisas: bool = False,
    ) -> List[Movimiento]:

        listaMovimientos = []

        def crearMovimiento(row, tipoDeCambio, comision, numero, precio):
            stringFecha = row[l(T_FECHA)]
            dia, mes, año = stringFecha.split("-")
            stringHora = row[l(T_HORA)]
            hora, minutos = stringHora.split(":")
            return Movimiento(
                fecha=date(int(año), int(mes), int(dia)),
                hora=time(int(hora), int(minutos)),
                producto=row[l(T_PRODUCTO)],
                isin=row[l(T_ISIN)],
                bolsa=row[l(T_BOLSA)],
                numero=numero,
                precio=precio,
                divisa=row[l(T_DIVISA)],
                valorLocal=float(row[l(T_VALORLOCAL)].replace(",", ".")),
                valor=float(row[l(T_VALOR)].replace(",", ".")),
                tipoDeCambio=tipoDeCambio,
                comision=comision,
                total=float(row[l(T_TOTAL)].replace(",", ".")),
            )

        with open(transactionPath, newline="") as csvtransactions:
            reader = csv.reader(csvtransactions)
            next(reader)
            for row in (row for row in reader if row[l(T_DIVISA)] in listaDivisas):
                tipoDeCambio = (
                    1 / float(row[l(T_TIPODECAMBIO)].replace(",", "."))
                    if row[l(T_TIPODECAMBIO)]
                    else 1
                )
                comision = (
                    float(row[l(T_COMISION)].replace(",", "."))
                    if row[l(T_COMISION)]
                    else 0.0
                )

                if modoDivisas:
                    valorLocal = float(row[l(T_VALORLOCAL)].replace(",", "."))
                    numero = -1 if valorLocal > 0 else 1
                    precio = abs(valorLocal)
                    comision = 0.0
                else:
                    numero = round(float(row[l(T_NUMERO)]))
                    precio = float(row[l(T_PRECIO)].replace(",", "."))

                listaMovimientos.append(
                    crearMovimiento(row, tipoDeCambio, comision, numero, precio)
                )

        listaMovimientos.reverse()
        return listaMovimientos
