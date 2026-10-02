# Analizador de Ventas - TP1

Elementos de Programación IA y Low Code - 2C2026

## Objetivo

Aplicación de consola para un pequeño emprendimiento que permite registrar ventas de
productos, consultarlas y filtrarlas, calcular indicadores de negocio (ingresos totales,
promedio por venta, producto más vendido y categoría líder), importar ventas desde un
archivo CSV externo y generar un gráfico con la distribución de ingresos por categoría.

**Público objetivo:** un emprendedor que vende productos agrupados por categorías (por
ejemplo indumentaria y accesorios) y hoy no tiene ninguna herramienta que le calcule indicadores automáticamente.

El código está dividido en dos módulos: main.py, que solo maneja el menú y la interacción con el usuario, y funciones.py, 
que tiene toda la lógica real. Esto separa la interfaz de la lógica de negocio, así funciones.py se puede reutilizar o probar sin depender del menú.


## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `main.py` | Menú por consola y flujo principal de la aplicación. |
| `funciones.py` | Funciones propias: persistencia, validación, búsqueda, modificación/eliminación, indicadores y gráfico. |
| `analisis.ipynb` | Exploración de los datos con pandas, gráficos y conclusiones. |
| `ventas.json` | Datos persistidos de las ventas (se crea/actualiza automáticamente). |
| `ventas_nuevas.csv` | Archivo externo de ejemplo para probar la importación (incluye una fila inválida a propósito, para ver la validación en acción). |
| `ventas_categoria.png` | Gráfico generado por la aplicación. |
| `requirements.txt` | Dependencias externas del proyecto. |
| `prompts_ia.md` | Registro de prompts usados con IA durante el desarrollo. |


## Cómo este proyecto cumple la consigna

**Funcionamiento mínimo:**

| Requisito de la consigna | Dónde está resuelto |
|---|---|
| 1. Cargar, obtener o recuperar información | `cargar_ventas()` lee `ventas.json` al iniciar |
| 2. Validar datos y responder ante errores | `validar_venta()`, `modificar_venta()` y `_estructura_venta_valida()` |
| 3. Consultar, buscar, filtrar o modificar registros | `buscar_por_producto()`, `filtrar_por_categoria()`, `gestionar_ventas()` |
| 4. Calcular al menos 3 indicadores útiles | `calcular_indicadores()`: ingresos totales, promedio por venta, producto más vendido, categoría líder (4 indicadores) |
| 5. Guardar/recuperar vía JSON, CSV o API | `guardar_ventas()` (JSON) + `importar_desde_csv()` (CSV externo) |
| 6. Al menos una visualización clara | `generar_grafico()` (matplotlib) + gráficos adicionales en `analisis.ipynb` |

**Requisitos técnicos:** variables, tipos, condiciones y bucles en todo `main.py` y
`funciones.py`; listas y diccionarios (cada venta es un diccionario dentro de una lista);
más de cuatro funciones propias con anotaciones de tipo; manejo de errores con
`try/except` en validación, conversión numérica y lectura/escritura de archivos; código
organizado en dos módulos (`main.py` y `funciones.py`); persistencia en JSON; uso de
pandas para los indicadores; un gráfico con matplotlib; y una fuente de datos externa
(`ventas_nuevas.csv`).


## Instalación

Ubicarse dentro de la carpeta Proyecto y correr los siguientes comandos:

**Windows:**
```
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Posibles errores en la instalación

### Versión de Python incompatible

El proyecto requiere **Python 3.10 o superior**. Puedes verificar tu versión actual con:

```bash
python3 --version
```

Si tienes una versión anterior (por ejemplo, Python 3.9), recomendamos instalar una versión más reciente utilizando `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc

uv python install 3.12
```

Luego, desde la raíz del proyecto, crea nuevamente el entorno virtual utilizando Python 3.12:

```bash
rm -rf .venv
uv venv --python 3.12 .venv
source .venv/bin/activate
```

Verifica que se esté utilizando la versión correcta:

```bash
python --version
```

El resultado debe indicar **Python 3.10 o superior**.

### `pip: command not found`

Si al instalar las dependencias aparece:

```text
command not found: pip
```

instala `pip` dentro del entorno virtual:

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

Finalmente, instala las dependencias del proyecto:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```
python main.py
```

El programa muestra un menú con 7 opciones: registrar venta, buscar/filtrar, modificar/eliminar venta, ver
indicadores, generar gráfico, importar CSV y salir.

### Ejemplo de uso

```
----- ANALIZADOR DE VENTAS (TP1) -----
1. Registrar nueva venta
2. Modificar o eliminar una venta
3. Buscar / filtrar ventas
4. Ver indicadores (Pandas)
5. Generar gráfico (Matplotlib)
6. Importar ventas desde CSV externo
7. Salir

Seleccioná una opción: 4

==================================
      RESUMEN ESTRATÉGICO
==================================
Operaciones registradas : 12
Ingresos totales        : $466.500,00
Promedio por venta      : $38.875,00
Producto más vendido    : Gorra
Categoría líder ($)     : Indumentaria
==================================
```

Para ver el análisis exploratorio, abrir `analisis.ipynb` con Jupyter:
```
jupyter notebook analisis.ipynb
```

## Decisiones principales

- **Dos módulos separados**: `main.py` solo maneja la interacción con el usuario (inputs,
  menú); toda la lógica (validación, cálculos, persistencia, gráfico) vive en `funciones.py`.
  Esto separa la ejecución principal de la lógica reutilizable, como pide la consigna.
- **Persistencia en JSON**: se eligió JSON porque conserva los tipos de datos (float, int,
  str) sin necesitar conversión manual al volver a cargarlos, a diferencia de un TXT plano.
- **Validación reforzada**: además de rechazar texto no numérico o valores negativos con
  `try/except`, `validar_venta()` usa `math.isfinite()` para descartar infinito/NaN y
  protege el cálculo del total contra `OverflowError`. Al cargar `ventas.json`,
  `_estructura_venta_valida()` revisa cada registro (campos presentes, tipos correctos,
  y que `total_venta` coincida con `precio * cantidad`) antes de aceptarlo, para que un
  archivo editado a mano o corrupto no rompa el programa.
- **Modificar y eliminar por número de posición**: como la aplicación no maneja un ID
  persistente para cada venta, `listar_ventas_numeradas()` muestra la lista enumerada y el
  usuario elige un número, que se valida como entero dentro de rango. Antes de eliminar se
  pide una confirmación explícita ("s/n") para evitar borrados accidentales.
- **Fuente de datos externa**: además del JSON propio, la app puede importar ventas desde un
  CSV externo (`importar_desde_csv`), simulando una fuente de datos ajena al programa (por
  ejemplo, una planilla del emprendimiento). Se valida que el CSV tenga las columnas
  correctas y cada fila se valida con la misma `validar_venta()` que usa el alta manual; las
  filas inválidas se descartan y se informan por consola.
- **Indicadores con pandas**: `calcular_indicadores` arma un DataFrame a partir de la lista
  de ventas y usa `sum()`, `mean()` y `groupby().idxmax()` para obtener los indicadores,
  evitando bucles manuales.
- **Gráfico con matplotlib**: se generan ingresos por categoría en un gráfico de barras,
  tanto desde `main.py` (opción 5) como desde el notebook.

## Cómo se comprobó que el código funciona

- Se ejecutó `main.py` de punta a punta probando cada opción del menú (registrar venta con
  datos válidos e inválidos, buscar por producto, filtrar por categoría, modificar y eliminar
  ventas según su número de orden en la lista, calcular indicadores, generar el gráfico e
  importar el CSV de ejemplo).
- Se verificó que los datos ingresados persisten correctamente reabriendo `ventas.json`
  después de cerrar y volver a ejecutar el programa.
- Se probó intencionalmente el manejo de errores ingresando texto en los campos de precio y
  cantidad, valores negativos, infinito y números extremadamente grandes, confirmando que el
  programa avisa el error sin cerrarse.
- Se editó `ventas.json` a mano con un campo faltante para confirmar que
  `_estructura_venta_valida()` lo detecta y el programa arranca con una lista vacía en vez de
  romperse.
- Se corrió la importación con `ventas_nuevas.csv`, que incluye una fila con precio negativo
  a propósito, para confirmar que se descarta esa fila y se agregan solo las válidas.
- Se ejecutó `analisis.ipynb` de principio a fin (Run All) para confirmar que los cálculos y
  los gráficos coinciden con los que muestra `main.py`.

## Prompts utilizados en el proyecto
Links prompts

