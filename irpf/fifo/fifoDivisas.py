import copy
from collections import defaultdict, deque
from typing import List, Deque

from irpf.fifo.fifo import Fifo
from irpf.modelo.movimiento import Movimiento
from irpf.modelo.transaccion import Transaccion


class FifoDivisas(Fifo):

    def crearDiccionarios(self):
        self.transacciones: defaultdict[str, List[Transaccion]] = defaultdict(list)
        self.asientos: defaultdict[str, Deque[Movimiento]] = defaultdict(deque)

    def obtencionCompraOVenta(self, entrada: Movimiento) -> bool:
        return entrada.valorLocal > 0

    def introducirAsiento(self, entrada: Movimiento):
        self.asientos[entrada.divisa].appendleft(entrada)

    def obtencionDeque(self, entrada: Movimiento) -> Deque[Movimiento]:
        return self.asientos[entrada.divisa]

    def condicionPositiva(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return entrada.valorLocal + compra.valorLocal < -0.5

    def transaccionPositiva(self, compra: Movimiento, entrada: Movimiento):

        transmision = copy.deepcopy(entrada)
        transmision.precio = compra.precio
        transmision.comision = (
            transmision.comision * transmision.precio / entrada.precio
        )
        super().recalcularMovimiento(transmision)
        transaccion = Transaccion(compra, transmision)

        entrada.precio -= compra.precio
        entrada.comision -= transmision.comision
        super().recalcularMovimiento(entrada)

        self.transacciones[entrada.divisa].append(transaccion)

    def condicionIgual(self, compra: Movimiento, entrada: Movimiento) -> bool:
        return round(entrada.precio + compra.precio) == 0

    def transaccionIgual(self, compra: Movimiento, entrada: Movimiento):

        transaccion = Transaccion(compra, entrada)
        self.transacciones[entrada.divisa].append(transaccion)

    def transaccionNegativa(self, compra: Movimiento, entrada: Movimiento):

        adquisicion = copy.deepcopy(compra)
        adquisicion.precio = entrada.precio
        adquisicion.comision = adquisicion.comision * adquisicion.precio / compra.precio
        super().recalcularMovimiento(adquisicion)
        transaccion = Transaccion(adquisicion, entrada)

        compra.precio -= entrada.precio
        compra.comision -= adquisicion.comision
        super().recalcularMovimiento(compra)

        self.transacciones[entrada.divisa].append(transaccion)

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
        errorSinCompra = super().algoritmoFIFO(
            añoRenta,
            listaMovimientos=listaMovimientos,
        )

        return self.transacciones, self.asientos, errorSinCompra
