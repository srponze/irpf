from typing import List

from irpf.modelo.movimiento import Movimiento


class Comisiones:

    @staticmethod
    def prorratear(listaMovimientos: List[Movimiento]):

        listaMovProrratear :List[Movimiento] = [listaMovimientos[0]]
        for movimiento in listaMovimientos:
            if round(movimiento.comision,2) != 0:
                if len(listaMovProrratear) != 1:
                    numeroTotal = sum(mov.numero for mov in listaMovProrratear)
                    comisionAProrratear = listaMovProrratear[0].comision
                    for movProrratear in listaMovProrratear:
                        movProrratear.comision = comisionAProrratear * movProrratear.numero / numeroTotal

                listaMovProrratear.clear()
                listaMovProrratear.append(movimiento)
            else:
                listaMovProrratear.append(movimiento)