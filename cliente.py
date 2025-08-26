from irpf.manager import Manager

accountPath = "Ruta/al/informe/account/de/Degiro"
transactionPath = "Ruta/al/informe/transaction/de/Degiro"
añoRenta = 2025

manager = Manager(
    transactionPath=transactionPath,
    accountPath=accountPath,
    añoRenta=añoRenta,
    realizarAcciones=True,  # Realiza los calculos de acciones
    agruparAcciones=False,  # Agrupa las acciones en solo una transaccion por valor, sumando todas las compras y ventas de dicho valor
    imprimirMovAcciones=True,  # Imprime los movimientos de acciones
    imprimirTransAcciones=True,  # Imprime las transacciones de acciones
    realizarDivisas=True,  # Realiza los calculos de divisas
    imprimirMovDivisas=True,  # Imprime los movimientos de divisas
    imprimirTransDivisas=True,  # Imprime las transacciones de divisas
    # Introduccion de ganancias en Renta Web
    introducirRenta=True,  # Introduce los datos en la web de la renta
    modoSimulador=False,  # Introduce los datos en una simulacion de Renta Web, en vez de iniciar sesion
    headless=False,  # Modo sin interfaz grafica
    tiempoDeEspera=150,  # Tiempo de espera (ms) para que se introduzcan los datos correctamente, si falla aumentar tiempo
)
