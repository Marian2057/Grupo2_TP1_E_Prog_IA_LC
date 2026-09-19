"""
main.py
Analizador de Ventas - TP1
Punto de entrada del programa. Maneja el menú por consola y llama a
las funciones definidas en funciones.py. No contiene lógica de negocio
propia: solo coordina la interacción con el usuario.
"""

from funciones import (
    cargar_ventas,
    guardar_ventas,
    validar_venta,
    agregar_venta,
    buscar_por_producto,
    filtrar_por_categoria,
    importar_desde_csv,
    calcular_indicadores,
    mostrar_indicadores,
    generar_grafico,
)

RUTA_DATOS = "ventas.json"
RUTA_GRAFICO = "ventas_categoria.png"


def mostrar_menu() -> None:
    print("\n----- ANALIZADOR DE VENTAS (TP1) -----")
    print("1. Registrar nueva venta")
    print("2. Buscar / filtrar ventas")
    print("3. Ver indicadores (Pandas)")
    print("4. Generar gráfico (Matplotlib)")
    print("5. Importar ventas desde CSV externo")
    print("6. Salir")


def registrar_venta(ventas: list[dict]) -> list[dict]:
    producto = input("Producto: ")
    categoria = input("Categoría: ")
    precio = input("Precio unitario: ")
    cantidad = input("Cantidad vendida: ")

    venta = validar_venta(producto, categoria, precio, cantidad)
    if venta is not None:
        ventas = agregar_venta(ventas, venta)
        guardar_ventas(ventas, RUTA_DATOS)
        print("[OK] Venta registrada y guardada.")
    return ventas


def consultar_ventas(ventas: list[dict]) -> None:
    print("\n1. Buscar por nombre de producto")
    print("2. Filtrar por categoría")
    sub_opcion = input("Elegí una opción: ")

    if sub_opcion == "1":
        texto = input("Nombre (o parte del nombre) del producto: ")
        resultado = buscar_por_producto(ventas, texto)
    elif sub_opcion == "2":
        categoria = input("Categoría: ")
        resultado = filtrar_por_categoria(ventas, categoria)
    else:
        print("[!] Opción no reconocida.")
        return

    if not resultado:
        print("No se encontraron ventas con ese criterio.")
        return

    for v in resultado:
        print(f" - {v['producto']} | {v['categoria']} | ${v['precio']:.2f} x {v['cantidad']} = ${v['total_venta']:.2f}")


def importar_csv(ventas: list[dict]) -> list[dict]:
    ruta_csv = input("Ruta del archivo CSV a importar (ej: ventas_nuevas.csv): ").strip()
    nuevas = importar_desde_csv(ruta_csv)
    if nuevas:
        ventas.extend(nuevas)
        guardar_ventas(ventas, RUTA_DATOS)
        print(f"[OK] Se importaron {len(nuevas)} ventas nuevas desde '{ruta_csv}'.")
    else:
        print("[!] No se importó ninguna venta válida.")
    return ventas


def main() -> None:
    ventas: list[dict] = cargar_ventas(RUTA_DATOS)

    while True:
        mostrar_menu()
        opcion = input("\nSeleccioná una opción: ")

        if opcion == "1":
            ventas = registrar_venta(ventas)
        elif opcion == "2":
            consultar_ventas(ventas)
        elif opcion == "3":
            indicadores = calcular_indicadores(ventas)
            mostrar_indicadores(indicadores)
        elif opcion == "4":
            generar_grafico(ventas, RUTA_GRAFICO)
        elif opcion == "5":
            ventas = importar_csv(ventas)
        elif opcion == "6":
            print("Cerrando el sistema...")
            break
        else:
            print("[!] Opción no reconocida. Elegí un número del 1 al 6.")


if __name__ == "__main__":
    main()
