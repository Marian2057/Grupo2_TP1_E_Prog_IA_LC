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
            return json.load(f)
    except (json.JSONDecodeError, OSError) as error:
        print(f"[!] No se pudo leer '{ruta}': {error}. Se empieza con una lista vacía.")
        return []


def guardar_ventas(ventas: list[dict], ruta: str) -> None:
    """Guarda la lista de ventas en un archivo JSON, con indentación legible."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(ventas, f, indent=4, ensure_ascii=False)


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

    try:
        precio: float = float(precio_texto)
        cantidad: int = int(cantidad_texto)
    except ValueError:
        print("[X] Error: precio y cantidad deben ser valores numéricos.")
        return None

    if precio <= 0 or cantidad <= 0:
        print("[!] El precio y la cantidad deben ser mayores a cero.")
        return None

    return {
        "producto": producto.strip().title(),
        "categoria": categoria.strip().title(),
        "precio": round(precio, 2),
        "cantidad": cantidad,
        "total_venta": round(precio * cantidad, 2),
    }


def agregar_venta(ventas: list[dict], venta: dict) -> list[dict]:
    """Agrega una venta ya validada a la lista y devuelve la lista actualizada."""
    ventas.append(venta)
    return ventas


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
            lector = csv.DictReader(f)
            for fila in lector:
                venta = validar_venta(
                    fila.get("producto", ""),
                    fila.get("categoria", ""),
                    fila.get("precio", "0"),
                    fila.get("cantidad", "0"),
                )
                if venta is not None:
                    nuevas.append(venta)
    except OSError as error:
        print(f"[X] Error al leer el CSV: {error}")

    return nuevas


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
    producto_top: str = df.groupby("producto")["cantidad"].sum().idxmax()
    categoria_top: str = df.groupby("categoria")["total_venta"].sum().idxmax()
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
    plt.savefig(ruta_salida)
    plt.close()

    print(f"\n[OK] Gráfico exportado como '{ruta_salida}'.")
    return True
