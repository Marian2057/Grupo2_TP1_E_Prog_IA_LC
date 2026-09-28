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
    listar_ventas_numeradas,
    eliminar_venta,
    modificar_venta,
)

RUTA_DATOS = "ventas.json"
RUTA_GRAFICO = "ventas_categoria.png"


def mostrar_menu() -> None:
    print("\n----- ANALIZADOR DE VENTAS (TP1) -----")
    print("1. Registrar nueva venta")
    print("2. Modificar o eliminar una venta")
    print("3. Buscar / filtrar ventas")
    print("4. Ver indicadores (Pandas)")
    print("5. Generar gráfico (Matplotlib)")
    print("6. Importar ventas desde CSV externo")
    print("7. Salir")


def registrar_venta(ventas: list[dict]) -> list[dict]:
    producto = input("Producto: ")
    categoria = input("Categoría: ")
    precio = input("Precio unitario: ")
    cantidad = input("Cantidad vendida: ")

    venta = validar_venta(producto, categoria, precio, cantidad)
    if venta is not None:
        ventas_actualizadas = agregar_venta(ventas.copy(), venta)
        if guardar_ventas(ventas_actualizadas, RUTA_DATOS):
            ventas = ventas_actualizadas
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


def gestionar_ventas(ventas: list[dict]) -> list[dict]:
    listar_ventas_numeradas(ventas)
    if not ventas:
        return ventas

    print("\n1. Modificar una venta")
    print("2. Eliminar una venta")
    sub_opcion = input("Elegí una opción: ")

    if sub_opcion not in ("1", "2"):
        print("[!] Opción no reconocida.")
        return ventas

    try:
        numero = int(input(f"Número de venta (1 a {len(ventas)}): "))
        indice = numero - 1
        if indice < 0 or indice >= len(ventas):
            print("[!] El número ingresado está fuera del rango.")
            return ventas
    except ValueError:
        print("[X] Error: ingresá un número entero.")
        return ventas

    if sub_opcion == "2":
        confirmacion = input(f"¿Seguro que querés eliminar '{ventas[indice]['producto']}'? (s/n): ")
        if confirmacion.strip().lower() == "s":
            ventas_actualizadas = eliminar_venta(ventas, indice)
            if guardar_ventas(ventas_actualizadas, RUTA_DATOS):
                print(f"[OK] Venta de '{ventas[indice]['producto']}' eliminada correctamente.")
                ventas = ventas_actualizadas
            else:
                print("[!] No se eliminó la venta porque no se pudo guardar el archivo.")
        else:
            print("[!] Eliminación cancelada.")
    else:
        print(f"Venta actual: {ventas[indice]['producto']} | "
              f"Precio: ${ventas[indice]['precio']:.2f} | "
              f"Cantidad: {ventas[indice]['cantidad']}")
        nuevo_precio = input("Nuevo precio unitario: ")
        nueva_cantidad = input("Nueva cantidad vendida: ")
        ventas_actualizadas = modificar_venta(ventas, indice, nuevo_precio, nueva_cantidad)
        if ventas_actualizadas is not None:
            if guardar_ventas(ventas_actualizadas, RUTA_DATOS):
                print(f"[OK] Venta de '{ventas[indice]['producto']}' actualizada correctamente.")
                ventas = ventas_actualizadas
            else:
                print("[!] No se modificó la venta porque no se pudo guardar el archivo.")

    return ventas


def importar_csv(ventas: list[dict]) -> list[dict]:
    ruta_csv = input("Ruta del archivo CSV a importar (ej: ventas_nuevas.csv): ").strip()
    nuevas = importar_desde_csv(ruta_csv)
    if nuevas:
        ventas_actualizadas = ventas + nuevas
        if guardar_ventas(ventas_actualizadas, RUTA_DATOS):
            ventas = ventas_actualizadas
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
            ventas = gestionar_ventas(ventas)
        elif opcion == "3":
            consultar_ventas(ventas)
        elif opcion == "4":
            indicadores = calcular_indicadores(ventas)
            mostrar_indicadores(indicadores)
        elif opcion == "5":
            generar_grafico(ventas, RUTA_GRAFICO)
        elif opcion == "6":
            ventas = importar_csv(ventas)
        elif opcion == "7":
            print("Cerrando el sistema...")
            break
        else:
            print("[!] Opción no reconocida. Elegí un número del 1 al 7.")


if __name__ == "__main__":
    main()
