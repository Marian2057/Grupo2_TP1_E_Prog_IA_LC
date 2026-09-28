# Analizador de Ventas - TP1

Elementos de Programación IA y Low Code - 2C2026

## Objetivo

Aplicación de consola para un pequeño emprendimiento que permite registrar ventas de
productos, consultarlas y filtrarlas, calcular indicadores de negocio (ingresos totales,
promedio por venta, producto más vendido y categoría líder), importar ventas desde un
archivo CSV externo y generar un gráfico con la distribución de ingresos por categoría.

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
- **Validación con try/except**: `validar_venta` controla que precio y cantidad sean
  numéricos y positivos, y devuelve `None` ante cualquier dato inválido en lugar de romper
  el programa.
- **Fuente de datos externa**: además del JSON propio, la app puede importar ventas desde un
  CSV externo (`importar_desde_csv`), simulando una fuente de datos ajena al programa (por
  ejemplo, una planilla del emprendimiento). Las filas inválidas del CSV se descartan y se
  informan por consola.
- **Indicadores con pandas**: `calcular_indicadores` arma un DataFrame a partir de la lista
  de ventas y usa `sum()`, `mean()` y `groupby().idxmax()` para obtener los indicadores,
  evitando bucles manuales.
- **Gráfico con matplotlib**: se generan ingresos por categoría en un gráfico de barras,
  tanto desde `main.py` (opción 5) como desde el notebook.

## Cómo se comprobó que el código funciona

- Se ejecutó `main.py` de punta a punta probando cada opción del menú (registrar venta con
  datos válidos e inválidos, buscar por producto, filtrar por categoría, modificar y eliminar ventas por ID, calcular
  indicadores, generar el gráfico e importar el CSV de ejemplo).
- Se verificó que los datos ingresados persisten correctamente reabriendo `ventas.json`
  después de cerrar y volver a ejecutar el programa.
- Se probó intencionalmente el manejo de errores ingresando texto en los campos de precio y
  cantidad, y valores negativos, confirmando que el programa avisa el error sin cerrarse.
- Se corrió `ventas_nuevas.csv`, que incluye una fila con precio negativo a propósito, para
  confirmar que la importación descarta esa fila y agrega solo las válidas.
- Se ejecutó `analisis.ipynb` de principio a fin (Run All) para confirmar que los cálculos y
  los gráficos coinciden con los que muestra `main.py`.
