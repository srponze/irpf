import csv
from datetime import date, time
from typing import List

from irpf.constantes.columnasInformes import *
from irpf.modelo.movimiento import Movimiento


class CSVDivisas:

    def obtenerDivisas(self, listaDivisasSinEur: List[str], accountPath: str):
        listaMovimientos = []

        def crearMovimiento(row, producto, numero):
            stringFecha = row[l(A_FECHA)]
            dia, mes, año = stringFecha.split("-")
            stringHora = row[l(A_HORA)]
            hora, minutos = stringHora.split(":")

            precio = abs(float(row[l(A_VARIACION)].replace(",", ".")))
            valorLocal = -precio * numero
            tipoDeCambio = 1 / float(row[l(A_TIPODECAMBIO)].replace(",", "."))
            valor = valorLocal * tipoDeCambio
            total = valor + 10
            return Movimiento(
                fecha=date(int(año), int(mes), int(dia)),
                hora=time(int(hora), int(minutos)),
                producto=producto,  # Ingreso o Compra de Divisa
                # Pone lo mismo que producto, pero sin puntos suspensivos
                isin=row[l(A_PRODUCTO)],
                bolsa="",
                numero=numero,
                precio=precio,
                divisa=row[l(A_DIVISA)],
                valorLocal=valorLocal,
                valor=valor,
                tipoDeCambio=tipoDeCambio,
                comision=-10,
                total=total,
            )

        with open(accountPath, newline="") as csvaccount:
            reader = csv.reader(csvaccount)
            next(reader)
            for row in (
                row for row in reader if row[l(A_DIVISA)] in listaDivisasSinEur
            ):
                if row[l(A_TIPODECAMBIO)] != "":

                    if float(row[l(A_VARIACION)].replace(",", ".")) > 0:
                        producto = "Ingreso"
                        numero = -1
                    else:
                        producto = "Retirada"
                        numero = 1

                    listaMovimientos.append(crearMovimiento(row, producto, numero))

        listaMovimientos.reverse()
        return listaMovimientos
