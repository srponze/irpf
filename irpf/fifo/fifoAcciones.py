import copy
from collections import defaultdict, deque
from typing import DefaultDict, List, Tuple, Deque

from irpf.fifo.fifo import Fifo
from irpf.modelo.movimiento import Movimiento
from irpf.modelo.transaccion import Transaccion


class FifoAcciones(Fifo):

    def crearDiccionarios(self):
        self.transacciones: DefaultDict[Tuple[str, str], List[Transaccion]] = (
            defaultdict(list)
        )
        self.asientos: DefaultDict[Tuple[str, str], Deque[Movimiento]] = defaultdict(
            deque
        )

    def obtencionCompraOVenta(self, entrada: Movimiento) -> bool:
        return entrada.numero > 0

    def introducirAsiento(self, entrada: Movimiento):
        self.asientos[(entrada.producto, entrada.bolsa)].appendleft(entrada)

    def obtencionDeque(self, entrada: Movimiento) -> Deque[Movimiento]:
        return self.asientos[(entrada.producto, entrada.bolsa)]

    def condicionPositiva(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return entrada.numero + compra.numero < 0

    def transaccionPositiva(self, compra: Movimiento, entrada: Movimiento):

        transmision = copy.deepcopy(entrada)
        transmision.numero = -compra.numero
        transmision.comision = (
            transmision.comision * transmision.numero / entrada.numero
        )
        super().recalcularMovimiento(transmision)
        transaccion = Transaccion(compra, transmision)

        entrada.numero += compra.numero
        entrada.comision -= transmision.comision
        super().recalcularMovimiento(entrada)

        self.transacciones[(entrada.producto, entrada.bolsa)].append(transaccion)

    def condicionIgual(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return entrada.numero + compra.numero == 0

    def transaccionIgual(self, compra: Movimiento, entrada: Movimiento):

        transaccion = Transaccion(compra, entrada)
        self.transacciones[(entrada.producto, entrada.bolsa)].append(transaccion)

    def transaccionNegativa(self, compra: Movimiento, entrada: Movimiento):

        adquisicion = copy.deepcopy(compra)
        adquisicion.numero = -entrada.numero
        adquisicion.comision = adquisicion.comision * adquisicion.numero / compra.numero
        super().recalcularMovimiento(adquisicion)
        transaccion = Transaccion(adquisicion, entrada)

        compra.numero += entrada.numero
        compra.comision -= adquisicion.comision
        super().recalcularMovimiento(compra)

        self.transacciones[(entrada.producto, entrada.bolsa)].append(transaccion)

    def borrarTransFueraDeAño(self, año: int):
        for key in self.transacciones:
            transaccionesBorrar = []
            for transaccion in self.transacciones[key]:
                if transaccion.transmision.fecha.year != self.añoRenta:
                    transaccionesBorrar.append(transaccion)

            if transaccionesBorrar:
                for fila in transaccionesBorrar:
                    self.transacciones[key].remove(fila)

    def algoritmoFIFO(self, añoRenta: int, listaMovimientos: List[Movimiento]):  # type: ignore[attr-defined]
        self.añoRenta = añoRenta

        errorsinCompra = super().algoritmoFIFO(
            añoRenta,
            listaMovimientos=listaMovimientos,
        )

        return self.transacciones, self.asientos, errorsinCompra
