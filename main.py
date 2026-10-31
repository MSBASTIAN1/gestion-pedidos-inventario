"""
C8T1 - Uso de Arreglos Unidimensionales en la solución de problemas reales
Reto 2: Sistema básico de gestión de pedidos e inventario
Autor: Michael Sebastián Ordóñez Tulcán

Programa principal: muestra el menú y llama a la función de cada opción.
Los datos se guardan en dos arreglos unidimensionales (listas):
    productos -> inventario
    pedidos   -> pedidos de los clientes
"""

import inventario as inv
import pedidos as ped
from utilidades import titulo


def cargar_datos_iniciales():
    """Retorna algunos productos de ejemplo para no empezar con el sistema vacío."""
    productos = [
        {"codigo": "P001", "nombre": "Teclado USB", "precio": 15.50, "stock": 20},
        {"codigo": "P002", "nombre": "Mouse inalámbrico", "precio": 12.00, "stock": 35},
        {"codigo": "P003", "nombre": "Monitor 24\"", "precio": 189.99, "stock": 6},
        {"codigo": "P004", "nombre": "Cable HDMI 2m", "precio": 6.75, "stock": 3},
    ]
    pedidos = []
    return productos, pedidos


def mostrar_resumen(productos, pedidos):
    """Reporte general del sistema."""
    titulo("RESUMEN GENERAL")
    pendientes = 0
    for p in pedidos:
        if p["estado"] == "Pendiente":
            pendientes += 1
    print(f"  Productos registrados:      {len(productos)}")
    print(f"  Valor total del inventario: ${inv.valor_total_inventario(productos):,.2f}")
    print(f"  Pedidos registrados:        {len(pedidos)} ({pendientes} pendientes)")
    print(f"  Total vendido (entregados): ${ped.total_vendido(pedidos):,.2f}")


# Cada opción del menú apunta a una función. Para agregar una funcionalidad
# nueva solo se agrega una línea aquí (el programa es escalable).
MENU = [
    ("1", "Registrar producto", lambda pr, pe: inv.registrar_producto(pr)),
    ("2", "Mostrar productos", lambda pr, pe: inv.mostrar_productos(pr)),
    ("3", "Editar producto", lambda pr, pe: inv.editar_producto(pr)),
    ("4", "Eliminar producto", lambda pr, pe: inv.eliminar_producto(pr, pe)),
    ("5", "Registrar pedido", lambda pr, pe: ped.registrar_pedido(pe, pr)),
    ("6", "Mostrar pedidos", lambda pr, pe: ped.mostrar_pedidos(pe, pr)),
    ("7", "Editar pedido", lambda pr, pe: ped.editar_pedido(pe, pr)),
    ("8", "Eliminar pedido", lambda pr, pe: ped.eliminar_pedido(pe, pr)),
    ("9", "Resumen general", mostrar_resumen),
]


ANCHO_MENU = 48


def linea_menu(texto):
    """Imprime una línea del menú dentro del recuadro."""
    print(f"│ {texto:<{ANCHO_MENU - 2}} │")


def mostrar_menu():
    print("\n┌" + "─" * ANCHO_MENU + "┐")
    linea_menu("SISTEMA DE GESTIÓN DE PEDIDOS E INVENTARIO".center(ANCHO_MENU - 2))
    print("├" + "─" * ANCHO_MENU + "┤")
    linea_menu(f"{'INVENTARIO':<24}PEDIDOS")
    for k in range(4):
        izq = f"{MENU[k][0]}. {MENU[k][1]}"
        der = f"{MENU[k + 4][0]}. {MENU[k + 4][1]}"
        linea_menu(f"{izq:<24}{der}")
    linea_menu(f"{MENU[8][0] + '. ' + MENU[8][1]:<24}0. Salir")
    print("└" + "─" * ANCHO_MENU + "┘")


def main():
    productos, pedidos = cargar_datos_iniciales()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            print("¡Hasta pronto!")
            break

        accion = None
        for clave, _, funcion in MENU:
            if clave == opcion:
                accion = funcion
                break

        if accion:
            accion(productos, pedidos)
        else:
            print("  ✗ Opción no válida.")


if __name__ == "__main__":
    main()
