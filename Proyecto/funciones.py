"""
funciones.py
Analizador de Ventas - TP1
Contiene las funciones reutilizables: carga y guardado de datos,
validación, búsqueda/filtrado, cálculo de indicadores y generación
de gráficos. main.py importa este módulo y arma el flujo principal.
"""

import json
import os
import csv
import math
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Persistencia de datos (JSON)
# ---------------------------------------------------------------------

def cargar_ventas(ruta: str) -> list[dict]:
    """Carga la lista de ventas desde un archivo JSON.

    Si el archivo no existe todavía, devuelve una lista vacía en vez
    de romper el programa (así la primera ejecución no falla).
    """
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            ventas = json.load(f)
        if not isinstance(ventas, list) or any(not _estructura_venta_valida(venta) for venta in ventas):
            print(f"[!] El archivo '{ruta}' no contiene una lista válida de ventas. Se empieza con una lista vacía.")
            return []
        return ventas
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as error:
        print(f"[!] No se pudo leer '{ruta}': {error}. Se empieza con una lista vacía.")
        return []


def _estructura_venta_valida(venta: object) -> bool:
    """Comprueba los campos y valores requeridos para una venta persistida."""
    if not isinstance(venta, dict):
        return False

    if not all(campo in venta for campo in ("producto", "categoria", "precio", "cantidad", "total_venta")):
        return False

    producto = venta["producto"]
    categoria = venta["categoria"]
    precio = venta["precio"]
    cantidad = venta["cantidad"]
    total_venta = venta["total_venta"]

    if not isinstance(producto, str) or not producto.strip():
        return False
    if not isinstance(categoria, str) or not categoria.strip():
        return False
    if isinstance(precio, bool) or not isinstance(precio, (int, float)):
        return False
    if isinstance(cantidad, bool) or not isinstance(cantidad, int):
        return False
    if isinstance(total_venta, bool) or not isinstance(total_venta, (int, float)):
        return False

    try:
        return (
            math.isfinite(precio)
            and precio > 0
            and cantidad > 0
            and math.isfinite(total_venta)
            and total_venta == round(precio * cantidad, 2)
        )
    except (OverflowError, TypeError):
        return False


def guardar_ventas(ventas: list[dict], ruta: str) -> bool:
    """Guarda ventas en JSON con indentación legible y devuelve False si ocurre un error de escritura."""
    try:
        contenido = json.dumps(ventas, indent=4, ensure_ascii=False, allow_nan=False)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return True
    except (OSError, TypeError, ValueError) as error:
        print(f"[X] No se pudieron guardar las ventas en '{ruta}': {error}")
        return False


# ---------------------------------------------------------------------
# Alta y validación de registros
# ---------------------------------------------------------------------

def validar_venta(producto: str, categoria: str, precio_texto: str, cantidad_texto: str) -> dict | None:
    """Valida los datos ingresados por consola y arma el registro de venta.

    Devuelve el diccionario de la venta si todo es correcto, o None si
    hay algún dato inválido (precio/cantidad no numéricos o negativos).
    """
    if not producto.strip() or not categoria.strip():
        print("[!] Producto y categoría no pueden estar vacíos.")
        return None

    resultado = _validar_precio_cantidad(precio_texto, cantidad_texto)
    if resultado is None:
        return None
    precio, cantidad, total_venta = resultado

    return {
        "producto": producto.strip().title(),
        "categoria": categoria.strip().title(),
        "precio": precio,
        "cantidad": cantidad,
        "total_venta": total_venta,
    }


def agregar_venta(ventas: list[dict], venta: dict) -> list[dict]:
    """Agrega una venta ya validada a la lista y devuelve la lista actualizada."""
    nueva = list(ventas)
    nueva.append(venta)
    return nueva


# ---------------------------------------------------------------------
# Consulta, búsqueda y filtrado
# ---------------------------------------------------------------------

def buscar_por_producto(ventas: list[dict], texto: str) -> list[dict]:
    """Devuelve las ventas cuyo producto contiene el texto buscado (sin importar mayúsculas)."""
    texto = texto.strip().lower()
    return [v for v in ventas if texto in v["producto"].lower()]


def filtrar_por_categoria(ventas: list[dict], categoria: str) -> list[dict]:
    """Devuelve solo las ventas de una categoría puntual."""
    categoria = categoria.strip().lower()
    return [v for v in ventas if v["categoria"].lower() == categoria]


# ---------------------------------------------------------------------
# Fuente de datos externa (importación desde CSV)
# ---------------------------------------------------------------------

def importar_desde_csv(ruta_csv: str) -> list[dict]:
    """Lee ventas desde un archivo CSV externo y las devuelve validadas.

    Sirve para incorporar en bloque ventas que vienen de otra fuente
    (por ejemplo, una planilla exportada por el emprendimiento).
    Las filas con datos inválidos se descartan y se avisa por consola.
    """
    nuevas: list[dict] = []
    if not os.path.exists(ruta_csv):
        print(f"[X] No se encontró el archivo '{ruta_csv}'.")
        return nuevas

    try:
        with open(ruta_csv, "r", encoding="utf-8", newline="") as f:
            lector = csv.DictReader(f, restkey="_campos_extra")
            campos_requeridos = {"producto", "categoria", "precio", "cantidad"}
            if lector.fieldnames is None or not campos_requeridos.issubset(lector.fieldnames):
                print(f"[X] El CSV debe incluir las columnas: {', '.join(sorted(campos_requeridos))}.")
                return nuevas

            for numero_fila, fila in enumerate(lector, start=2):
                if fila.get("_campos_extra") is not None or any(
                    fila.get(campo) is None for campo in campos_requeridos
                ):
                    print(f"[!] Se descarta la fila {numero_fila}: cantidad de columnas incorrecta.")
                    continue

                venta = validar_venta(
                    fila["producto"],
                    fila["categoria"],
                    fila["precio"],
                    fila["cantidad"],
                )
                if venta is not None:
                    nuevas.append(venta)
                else:
                    print(f"    ^ fila {numero_fila} descartada por datos inválidos.")
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        print(f"[X] Error al leer el CSV: {error}")

    return nuevas


# ---------------------------------------------------------------------
# Modificación y eliminación de registros
# ---------------------------------------------------------------------

def listar_ventas_numeradas(ventas: list[dict]) -> None:
    """Imprime todas las ventas con un número de índice para que el usuario
    pueda seleccionar cuál modificar o eliminar."""
    if not ventas:
        print("\n[!] No hay ventas registradas todavía.")
        return

    print("\n" + "-" * 60)
    for i, v in enumerate(ventas):
        print(f"  {i + 1}. {v['producto']} | {v['categoria']} | "
              f"${v['precio']:.2f} x {v['cantidad']} = ${v['total_venta']:.2f}")
    print("-" * 60)


def eliminar_venta(ventas: list[dict], indice: int) -> list[dict]:
    """Elimina la venta ubicada en la posición indicada (índice basado en 0).

    Devuelve la lista actualizada. La validación del rango debe hacerse
    antes de llamar a esta función.
    """
    ventas_actualizadas = ventas.copy()
    ventas_actualizadas.pop(indice)
    return ventas_actualizadas


def _validar_precio_cantidad(precio_texto: str, cantidad_texto: str) -> tuple[float, int, float] | None:
    """Valida y convierte precio y cantidad. Devuelve (precio, cantidad, total) o None si hay error."""
    try:
        precio: float = float(precio_texto)
        cantidad: int = int(cantidad_texto)
    except ValueError:
        print("[X] Error: precio y cantidad deben ser valores numéricos.")
        return None

    if not math.isfinite(precio):
        print("[!] El precio debe ser un número finito.")
        return None

    if precio <= 0 or cantidad <= 0:
        print("[!] El precio y la cantidad deben ser mayores a cero.")
        return None

    precio = round(precio, 2)
    if precio <= 0:
        print("[!] El precio debe ser de al menos $0.01 después del redondeo.")
        return None

    try:
        total_venta = round(precio * cantidad, 2)
    except OverflowError:
        print("[!] El total de la venta excede el rango permitido.")
        return None
    if not math.isfinite(total_venta):
        print("[!] El total de la venta debe ser un número finito.")
        return None

    return precio, cantidad, total_venta


def modificar_venta(ventas: list[dict], indice: int,
                    producto: str, categoria: str,
                    precio_texto: str, cantidad_texto: str) -> list[dict] | None:
    """Actualiza todos los campos de la venta en la posición indicada.

    Recalcula total_venta automáticamente. Devuelve la lista actualizada,
    o None si los nuevos datos son inválidos.
    """
    if not producto.strip() or not categoria.strip():
        print("[!] Producto y categoría no pueden estar vacíos.")
        return None

    resultado = _validar_precio_cantidad(precio_texto, cantidad_texto)
    if resultado is None:
        return None
    precio, cantidad, total_venta = resultado

    ventas_actualizadas = [venta.copy() for venta in ventas]
    ventas_actualizadas[indice]["producto"] = producto.strip().title()
    ventas_actualizadas[indice]["categoria"] = categoria.strip().title()
    ventas_actualizadas[indice]["precio"] = precio
    ventas_actualizadas[indice]["cantidad"] = cantidad
    ventas_actualizadas[indice]["total_venta"] = total_venta
    return ventas_actualizadas


# ---------------------------------------------------------------------
# Análisis con pandas (indicadores)
# ---------------------------------------------------------------------

def calcular_indicadores(ventas: list[dict]) -> dict:
    """Calcula indicadores del negocio usando pandas.

    Devuelve un diccionario con: ingresos totales, promedio por venta,
    producto más vendido (por cantidad) y categoría con mayores ingresos.
    """
    if not ventas:
        return {}

    df = pd.DataFrame(ventas)

    ingresos_totales: float = float(df["total_venta"].sum())
    promedio_venta: float = float(df["total_venta"].mean())

    cant_por_producto = df.groupby("producto")["cantidad"].sum()
    max_cant = cant_por_producto.max()
    producto_top: str = ", ".join(cant_por_producto[cant_por_producto == max_cant].index.tolist())

    ing_por_categoria = df.groupby("categoria")["total_venta"].sum()
    max_ing = ing_por_categoria.max()
    categoria_top: str = ", ".join(ing_por_categoria[ing_por_categoria == max_ing].index.tolist())

    cantidad_operaciones: int = int(len(df))

    return {
        "ingresos_totales": round(ingresos_totales, 2),
        "promedio_venta": round(promedio_venta, 2),
        "producto_top": producto_top,
        "categoria_top": categoria_top,
        "cantidad_operaciones": cantidad_operaciones,
    }


def mostrar_indicadores(indicadores: dict) -> None:
    """Imprime por consola los indicadores calculados con un formato prolijo."""
    if not indicadores:
        print("\n[!] No hay datos suficientes para analizar todavía.")
        return

    print("\n" + "=" * 34)
    print("      RESUMEN ESTRATÉGICO")
    print("=" * 34)
    print(f"Operaciones registradas : {indicadores['cantidad_operaciones']}")
    print(f"Ingresos totales        : ${indicadores['ingresos_totales']:,.2f}")
    print(f"Promedio por venta      : ${indicadores['promedio_venta']:,.2f}")
    print(f"Producto más vendido    : {indicadores['producto_top']}")
    print(f"Categoría líder ($)     : {indicadores['categoria_top']}")
    print("=" * 34)


# ---------------------------------------------------------------------
# Visualización con matplotlib
# ---------------------------------------------------------------------

def generar_grafico(ventas: list[dict], ruta_salida: str) -> bool:
    """Genera un gráfico de barras con los ingresos totales por categoría.

    Devuelve True si el gráfico se generó y guardó correctamente.
    """
    if not ventas:
        print("\n[!] No hay datos para graficar.")
        return False

    df = pd.DataFrame(ventas)
    ingresos_por_categoria = df.groupby("categoria")["total_venta"].sum().sort_values(ascending=False)

    plt.figure(figsize=(9, 5.5))
    ingresos_por_categoria.plot(kind="bar", color="#3498db", edgecolor="black")
    plt.title("Ingresos totales por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Ingresos ($)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    try:
        plt.savefig(ruta_salida)
    except OSError as error:
        plt.close()
        print(f"[X] No se pudo guardar el gráfico en '{ruta_salida}': {error}")
        return False
    plt.close()

    print(f"\n[OK] Gráfico exportado como '{ruta_salida}'.")
    return True
