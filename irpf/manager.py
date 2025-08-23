import traceback
from bisect import insort
from collections import defaultdict
from datetime import date, time
from typing import DefaultDict, List, Tuple

from irpf.csv.csvAcciones import CSVAcciones
from irpf.csv.csvDivisas import CSVDivisas
from irpf.csv.obtenerListaDivisas import ObtenerListaDivisas
from irpf.fifo.comisiones import Comisiones
from irpf.fifo.fifoAcciones import FifoAcciones
from irpf.fifo.fifoDivisas import FifoDivisas
from irpf.modelo.movimiento import Movimiento
from irpf.modelo.transaccion import Transaccion
from irpf.play import Play
from irpf.constantes.mensajesTerminal import *


class ManagerMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Manager(metaclass=ManagerMeta):

    def __init__(
        self,
        transactionPath: str,
        accountPath: str,
        añoRenta: int,
        realizarAcciones: bool = True,
        agruparAcciones: bool = False,
        imprimirMovAcciones: bool = False,
        imprimirTransAcciones: bool = False,
        realizarDivisas: bool = True,
        imprimirMovDivisas: bool = False,
        imprimirTransDivisas: bool = False,
        introducirRenta: bool = True,
        detectaDivisas: bool = True,
        channel: str = "chrome",
        headless: bool = False,
        modoSimulador: bool = False,
        tiempoDeEspera: int = 150,
    ):

        self.transactionPath: str = transactionPath
        self.accountPath: str = accountPath
        self.añoRenta: int = añoRenta
        self.realizarAcciones: bool = realizarAcciones
        self.agruparAcciones: bool = agruparAcciones
        self.imprimirMovAcciones: bool = imprimirMovAcciones
        self.imprimirTransAcciones: bool = imprimirTransAcciones
        self.realizarDivisas: bool = realizarDivisas
        self.imprimirMovDivisas: bool = imprimirMovDivisas
        self.imprimirTransDivisas: bool = imprimirTransDivisas
        self.introducirRenta: bool = introducirRenta
        self.detectaDivisas: bool = detectaDivisas
        self.channel: str = channel
        self.headless: bool = headless
        self.modoSimulador: bool = modoSimulador
        self.tiempoDeEspera: int = tiempoDeEspera

        self.transaccionesAcciones: DefaultDict[Tuple[str, str], List[Transaccion]] = (
            defaultdict(list)
        )
        self.transaccionesDivisas: DefaultDict[str, List[Transaccion]] = defaultdict(
            list
        )

        if self.detectaDivisas:
            self.listaDivisas = ObtenerListaDivisas.obtenerListaDivisas(
                self.transactionPath
            )
        self.listaDivisasSinEur = [
            divisa for divisa in self.listaDivisas if divisa != "EUR"
        ]

        if len(self.listaDivisas) == 0:
            raise Exception(
                "No se han encontrado divisas en transactions o las pasadas por config"
            )
        else:
            if self.generarListas() != True:
                raise Exception(
                    "No se ha seleccionado ninguna actividad (acciones, divisas o dividendos)"
                )
            else:
                if self.introducirRenta:
                    try:
                        self.play = Play()
                        self.play.iniciar(
                            channel=self.channel,
                            headless=self.headless,
                            modoSimulador=self.modoSimulador,
                            tiempoDeEspera=self.tiempoDeEspera,
                        )
                        if (
                            self.realizarAcciones
                            and len(self.transaccionesAcciones) != 0
                        ):
                            self.play.introducirAcciones(self.transaccionesAcciones)

                        if self.realizarDivisas and len(self.transaccionesDivisas) != 0:
                            self.play.introducirDivisas(self.transaccionesDivisas)

                        self.play.esperar()
                    finally:
                        self.play.close()

    def generarListas(self) -> bool:
        arrancar = False
        self.listaMovAcciones: List[Movimiento] = []
        self.listaMovDivisas: List[Movimiento] = []
        self.listaMovAccDivisas: List[Movimiento] = []
        self.listaMovCompletaDivisas: List[Movimiento] = []

        if self.realizarAcciones:
            arrancar = True
            self.realizarAcc()

        if self.realizarDivisas:
            arrancar = True
            self.realizarDiv()

        return arrancar

    def realizarAcc(self):
        self.csvAcciones = CSVAcciones()
        listaMovAcciones = self.csvAcciones.obtenerAcciones(
            self.listaDivisas, self.transactionPath
        )

        Comisiones.prorratear(listaMovAcciones)

        if self.imprimirMovAcciones and listaMovAcciones:
            print("\n####### MOVIMIENTOS DE ACCIONES #######")
            print(msgMovAcciones)
            for movimiento in listaMovAcciones:
                print(movimiento)

        fifoAcciones = FifoAcciones()
        listaTransacciones, listaAsientos, errorSinCompra = fifoAcciones.algoritmoFIFO(
            añoRenta=self.añoRenta, listaMovimientos=listaMovAcciones
        )
        if errorSinCompra:
            self.introducirRenta = False

        self.transaccionesAcciones.update(listaTransacciones)

        if self.imprimirMovAcciones and listaAsientos:
            print("\n####### POSICIONES DE ACCIONES A FINAL DEL PERIODO #######")
            print(msgMovAcciones)
            for key in listaAsientos:
                for movimiento in listaAsientos[key]:
                    print(movimiento)

        if self.agruparAcciones:
            self.agruparAcc()

        if self.imprimirTransAcciones and self.transaccionesAcciones:
            print("\n####### TRANSACCIONES DE ACCIONES #######")
            print(msgTransAcciones)
            for key in self.transaccionesAcciones:
                for transaccion in self.transaccionesAcciones[key]:
                    print(transaccion)

    def realizarDiv(self):
        self.csvDivisas = CSVDivisas()
        self.csvAcciones = CSVAcciones()

        listaMovDivisas = self.csvDivisas.obtenerDivisas(
            self.listaDivisasSinEur, self.accountPath
        )
        listaMovAccDivisas = self.csvAcciones.obtenerAcciones(
            self.listaDivisasSinEur, self.transactionPath, modoDivisas=True
        )

        # Unir listaMovDivisas y listaMovAccDivisas
        listaMovCompletaDivisas = listaMovAccDivisas
        for flujo in listaMovDivisas:
            insort(listaMovCompletaDivisas, flujo, key=lambda x: (x.fecha, x.hora))

        if self.imprimirMovDivisas and listaMovCompletaDivisas:
            print("\n####### MOVIMIENTOS DE DIVISAS #######")
            for movimiento in listaMovCompletaDivisas:
                print(movimiento)

        fifoDivisas = FifoDivisas()
        listaTransacciones, listaAsientos, errorSinCompra = fifoDivisas.algoritmoFIFO(
            añoRenta=self.añoRenta,
            listaMovimientos=listaMovCompletaDivisas,
        )
        if errorSinCompra:
            self.introducirRenta = False

        self.transaccionesDivisas.update(listaTransacciones)

        if self.imprimirMovDivisas and listaAsientos:
            print("\n####### POSICIONES DE DIVISAS A FINAL DEL PERIODO #######")
            for key in listaAsientos:
                for movimiento in listaAsientos[key]:
                    print(movimiento)

        if self.imprimirTransDivisas and self.transaccionesDivisas:
            print("\n####### TRANSACCIONES DE DIVISAS #######")
            for key in self.transaccionesDivisas:
                for transaccion in self.transaccionesDivisas[key]:
                    print(transaccion)

    def agruparAcc(self):
        transaccionesAgrupadas = defaultdict(list)
        for key in self.transaccionesAcciones:
            isin = self.transaccionesAcciones[key][0].adquisicion.isin
            divisa = self.transaccionesAcciones[key][0].adquisicion.divisa
            bolsa = self.transaccionesAcciones[key][0].adquisicion.bolsa
            producto = self.transaccionesAcciones[key][0].adquisicion.producto
            sumaTotalAdquisiciones = 0
            sumaTotalTransmisiones = 0
            sumaNumeroAdquisiciones = 0
            sumaNumeroTranmisiones = 0
            sumaComisionAdquisiciones = 0
            sumaComisionTransmisiones = 0
            for transaccion in self.transaccionesAcciones[key]:
                sumaTotalAdquisiciones += transaccion.adquisicion.total
                sumaTotalTransmisiones += transaccion.transmision.total
                sumaNumeroAdquisiciones += transaccion.adquisicion.numero
                sumaNumeroTranmisiones += transaccion.transmision.numero
                sumaComisionAdquisiciones += transaccion.adquisicion.comision
                sumaComisionTransmisiones += transaccion.transmision.comision

            transaccion = Transaccion(
                adquisicion=Movimiento(
                    date.today(),
                    time(0, 0),
                    isin=isin,
                    bolsa=bolsa,
                    producto=producto,
                    numero=sumaNumeroAdquisiciones,
                    precio=0,
                    valorLocal=0,
                    valor=0,
                    tipoDeCambio=0,
                    comision=sumaComisionAdquisiciones,
                    total=sumaTotalAdquisiciones,
                    divisa=divisa,
                ),
                transmision=Movimiento(
                    date.today(),
                    time(0, 0),
                    isin=isin,
                    bolsa=bolsa,
                    producto=producto,
                    numero=sumaNumeroTranmisiones,
                    precio=0,
                    valorLocal=0,
                    valor=0,
                    tipoDeCambio=0,
                    comision=sumaComisionTransmisiones,
                    total=sumaTotalTransmisiones,
                    divisa=divisa,
                ),
            )
            transaccionesAgrupadas[producto] = [transaccion]
        self.transaccionesAcciones = transaccionesAgrupadas
