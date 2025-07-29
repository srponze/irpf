from abc import ABC, abstractmethod
from typing import List, Deque

from irpf.modelo.movimiento import Movimiento
from irpf.modelo.transaccion import Transaccion


class Fifo(ABC):

    def algoritmoFIFO(
        self,
        añoRenta: int,
        listaMovimientos: List[Movimiento],
    ):
        self.crearDiccionarios()
        errorSinCompra = False

        for entrada in listaMovimientos:

            # Compra
            if self.obtencionCompraOVenta(entrada):
                # Se introduce la compra en el diccionario de asientos
                self.introducirAsiento(entrada)

            # Venta
            else:
                deq = self.obtencionDeque(entrada)
                while deq:
                    # Todavia queda valores o divisas en el movimiento entrada
                    if self.condicionPositiva(deq[-1], entrada):
                        self.transaccionPositiva(deq.pop(), entrada)

                        # El movimiento entrada se compensa con un movimiento compra
                    elif self.condicionIgual(deq[-1], entrada):
                        self.transaccionIgual(deq.pop(), entrada)
                        break

                        # Todavia queda valores o divisas en el movimiento compra
                    else:
                        self.transaccionNegativa(deq[-1], entrada)
                        break

                else:
                    errorSinCompra = True
                    print(
                        "\nPara esta venta no hay un movimiento de compra asociado \n",
                        entrada,
                    )
                    print("Por favor, revisa las fechas del informe de degiro.")

        # Eliminar las transacciones no transmitidas en el año
        self.borrarTransFueraDeAño(añoRenta)

        return errorSinCompra

    def recalcularMovimiento(self, movimiento: Movimiento):
        movimiento.valorLocal = -movimiento.numero * movimiento.precio
        movimiento.valor = movimiento.valorLocal * movimiento.tipoDeCambio
        movimiento.total = movimiento.valor + movimiento.comision

    @abstractmethod
    def crearDiccionarios(self):
        pass

    @abstractmethod
    def obtencionCompraOVenta(self, entrada: Movimiento) -> bool:
        pass

    @abstractmethod
    def introducirAsiento(self, entrada: Movimiento):
        pass

    @abstractmethod
    def obtencionDeque(self, entrada: Movimiento) -> Deque[Movimiento]:
        pass

    @abstractmethod
    def condicionPositiva(self, compra: Movimiento, entrada: Movimiento) -> bool:
        pass

    @abstractmethod
    def condicionIgual(self, compra: Movimiento, entrada: Movimiento) -> bool:
        pass

    @abstractmethod
    def transaccionPositiva(self, compra: Movimiento, entrada: Movimiento):
        pass

    @abstractmethod
    def transaccionIgual(self, compra: Movimiento, entrada: Movimiento):
        pass

    @abstractmethod
    def transaccionNegativa(self, compra: Movimiento, entrada: Movimiento):
        pass

    @abstractmethod
    def borrarTransFueraDeAño(self, año: int):
        pass
