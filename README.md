# CALCULO E INTRODUCCIÓN DE GANANCIAS Y PERDIDAS POR COMPRA-VENTA DE ACCIONES EN EL IRPF ESPAÑOL (RENTAWEB) EN DEGIRO

## Descripción
Esta aplicación sirve para calcular e introducir en rentaWeb las ganancias y perdidas patrimoniales producidas por compra-venta de acciones cotizadas tanto en euros como en otras divisas y teniendo en cuenta el metodo FIFO, para ello se sirve de los informes de estado de cuenta y transacciones que genera Degiro, tambien calcula la compra-venta de divisas implicita de las acciones cotizadas en otras divisas al euro. segun esta web: https://www.filios.app/blog/como-meter-las-operaciones-con-divisas-en-el-irpf/

Se debe de escoger el rango de fechas de los informes desde el momento de alguna compra de alguna accion que se haya vendido en el año del que se quiere calcular el irpf hasta el ultimo dia del año, por ejemplo: si queremos calcular el irpf de 2025 y en ese año hemos vendido alguna accion comprada en 2024 (según el metodo FIFO), debemos de incluirla en el informe, no te preocupes, el resto de las acciones compradas en 2024 no las tienes en cuenta. 

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/srponze/irpf.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd irpf
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r playwright
   ```

## Uso
1. Descarga los informes "estado de cuenta" y "transacciones" del broker Degiro apropiados para el año que queremos calcular en formato CSV, estan en Buzón.
2. Introduce en cliente.py la ruta de ambos informes y el año a calcular, y selecciona los parametros de la clase Manager
3. Ejecuta el script principal:
   ```bash
   python cliente.py
   ```

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

## Contacto
Para preguntas o soporte, contacta a [srponze](https://github.com/srponze).
