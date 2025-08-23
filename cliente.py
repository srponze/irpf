from irpf.manager import Manager

accountPath = "Ruta/al/informe/account/de/Degiro"
transactionPath = "Ruta/al/informe/transaction/de/Degiro"
añoRenta = 2025

manager = Manager(
    transactionPath=transactionPath,
    accountPath=accountPath,
    añoRenta=añoRenta,
    realizarAcciones=True,
    agruparAcciones=False,
    imprimirMovAcciones=True,
    imprimirTransAcciones=True,
    realizarDivisas=True,
    imprimirMovDivisas=True,
    imprimirTransDivisas=True,
    introducirRenta=False,
    modoSimulador=True,
)
