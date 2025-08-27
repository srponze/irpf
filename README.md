# Calculadora de Ganancias Patrimoniales para Renta Web

Esta herramienta simplifica la declaración de la renta para inversores. Automatiza el cálculo de las ganancias y pérdidas patrimoniales derivadas de la compra y venta de acciones cotizadas y ETF y las introduce en Renta Web.


## Características principales
Cálculo automático y preciso: La aplicación procesa tus informes de Degiro y determina las ganancias o pérdidas patrimoniales.

Método FIFO: Utiliza el método First-In, First-Out (FIFO) para cumplir con la normativa de la Agencia Tributaria Española.

Manejo de múltiples divisas: Calcula automáticamente las ganancias para acciones cotizadas en euros y en otras divisas, incluyendo la propia tributación de la tenencia de divisa extranjera, siguiendo este artículo https://www.filios.app/blog/como-meter-las-operaciones-con-divisas-en-el-irpf/

Datos listos para Renta Web: Genera los datos que necesitas para que autónomamente sean introducidos en Renta Web mediante el paquete playwright.
(Actualmente, solo pueden ser introducidos en una simulación de Renta Web, más adelante podrás introducirlos en tu propia sesión)


## Instalación
1. Clona este repositorio o descarga el archivo Zip y descomprímelo:
   ```bash
   git clone https://github.com/srponze/irpf.git
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install playwright
   ```


## Uso
1. Obtén los informes de "Estado de cuenta" y "Transacciones" de tu cuenta de Degiro en formato csv.
Asegúrate de que el rango de fechas de los informes cubra desde el momento de la primera compra de alguna de las acciones que has vendido en el año fiscal, hasta el último día de dicho año. Esto es crucial para que el método FIFO se aplique correctamente.

   Ej: Si en 2025 has vendido varias acciones compradas en 2024, aumenta el rango inicial hasta el momento de dicha compra, no te preocupes por el resto de acciones que no se hayan vendido en 2025 que incluyas, no se tendrán en cuenta

3. Mueve los archivos Account.csv y Transactions.csv al directorio donde hayas descargado el código 

4. Ejecuta el script cliente.py:
   ```bash
   python cliente.py
   ```


## Opciones
(Por documentar)


## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.


## Contacto
Para preguntas o soporte, contacta a [srponze](https://github.com/srponze).