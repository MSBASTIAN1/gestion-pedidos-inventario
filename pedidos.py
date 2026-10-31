"""
Módulo de pedidos.

Los pedidos también se guardan en un ARREGLO UNIDIMENSIONAL (lista).
Cada pedido es un diccionario:
    {"numero": 1, "cliente": "Ana", "codigo_producto": "P001",
     "cantidad": 2, "total": 31.0, "estado": "Pendiente"}

Al registrar un pedido se descuenta el stock del inventario y al eliminar
un pedido pendiente el stock se devuelve.
"""

from utilidades import leer_texto, leer_entero, confirmar, titulo
from inventario import buscar_producto

ESTADOS = ["Pendiente", "Entregado"]


def buscar_pedido(pedidos, numero):
    """Retorna el índice del pedido con ese número, o -1 si no existe."""
    for i in range(len(pedidos)):
        if pedidos[i]["numero"] == numero:
            return i
    return -1


def siguiente_numero(pedidos):
    """El número de pedido es el último número usado + 1."""
    return pedidos[-1]["numero"] + 1 if pedidos else 1


def registrar_pedido(pedidos, productos):
    """Registra un pedido validando que el producto exista y que haya stock."""
    titulo("REGISTRAR PEDIDO")
    if len(productos) == 0:
        print("  ✗ Primero debe registrar productos en el inventario.")
        return

    cliente = leer_texto("Nombre del cliente: ")
    i = buscar_producto(productos, leer_texto("Código del producto: "))
    if i == -1:
        print("  ✗ No existe un producto con ese código.")
        return

    producto = productos[i]
    print(f"  {producto['nombre']} - ${producto['precio']:.2f} - disponibles: {producto['stock']}")
    cantidad = leer_entero("Cantidad: ", minimo=1)
    if cantidad > producto["stock"]:
        print(f"  ✗ Stock insuficiente. Solo hay {producto['stock']} unidades.")
        return

    producto["stock"] -= cantidad
    pedido = {
        "numero": siguiente_numero(pedidos),
        "cliente": cliente,
        "codigo_producto": producto["codigo"],
        "cantidad": cantidad,
        "total": round(cantidad * producto["precio"], 2),
        "estado": "Pendiente",
    }
    pedidos.append(pedido)
    print(f"  ✓ Pedido #{pedido['numero']} registrado. Total: ${pedido['total']:.2f}")


def mostrar_pedidos(pedidos, productos):
    """Muestra todos los pedidos con el nombre del producto."""
    titulo("LISTADO DE PEDIDOS")
    if len(pedidos) == 0:
        print("  No hay pedidos registrados.")
        return

    print(f"  {'N°':<4} {'Cliente':<16} {'Producto':<18} {'Cant':>4} {'Total':>10}  Estado")
    print("  " + "-" * 64)
    for pedido in pedidos:
        i = buscar_producto(productos, pedido["codigo_producto"])
        nombre = productos[i]["nombre"] if i != -1 else "(eliminado)"
        print(f"  {pedido['numero']:<4} {pedido['cliente']:<16} {nombre:<18} "
              f"{pedido['cantidad']:>4} ${pedido['total']:>9.2f}  {pedido['estado']}")


def editar_pedido(pedidos, productos):
    """
    Permite cambiar la cantidad (solo si está pendiente) y el estado.
    Si cambia la cantidad, se ajusta el stock con la diferencia.
    """
    titulo("EDITAR PEDIDO")
    i = buscar_pedido(pedidos, leer_entero("Número de pedido: ", minimo=1))
    if i == -1:
        print("  ✗ No existe ese pedido.")
        return

    pedido = pedidos[i]
    j = buscar_producto(productos, pedido["codigo_producto"])
    print(f"  Pedido #{pedido['numero']} - {pedido['cliente']} - estado: {pedido['estado']} (Enter = mantener)")

    if pedido["estado"] == "Pendiente" and j != -1:
        producto = productos[j]
        nueva = leer_entero(f"Cantidad [{pedido['cantidad']}]: ", minimo=1, permitir_vacio=True)
        if nueva is not None:
            diferencia = nueva - pedido["cantidad"]
            if diferencia > producto["stock"]:
                print(f"  ✗ Stock insuficiente para aumentar (disponibles: {producto['stock']}).")
                return
            producto["stock"] -= diferencia
            pedido["cantidad"] = nueva
            pedido["total"] = round(nueva * producto["precio"], 2)

    print("  Estados: " + ", ".join(f"{k + 1}. {e}" for k, e in enumerate(ESTADOS)))
    opcion = leer_entero("Nuevo estado [Enter = mantener]: ", minimo=1, permitir_vacio=True)
    if opcion is not None and opcion <= len(ESTADOS):
        pedido["estado"] = ESTADOS[opcion - 1]
    print(f"  ✓ Pedido actualizado: {pedido['cantidad']} u., total ${pedido['total']:.2f}, {pedido['estado']}.")


def eliminar_pedido(pedidos, productos):
    """Elimina (cancela) un pedido. Si estaba pendiente, devuelve el stock."""
    titulo("ELIMINAR PEDIDO")
    i = buscar_pedido(pedidos, leer_entero("Número de pedido a eliminar: ", minimo=1))
    if i == -1:
        print("  ✗ No existe ese pedido.")
        return

    pedido = pedidos[i]
    if not confirmar(f"¿Eliminar el pedido #{pedido['numero']} de {pedido['cliente']}?"):
        print("  Operación cancelada.")
        return

    if pedido["estado"] == "Pendiente":
        j = buscar_producto(productos, pedido["codigo_producto"])
        if j != -1:
            productos[j]["stock"] += pedido["cantidad"]
            print(f"  Se devolvieron {pedido['cantidad']} unidades al inventario.")
    pedidos.pop(i)
    print(f"  ✓ Pedido #{pedido['numero']} eliminado.")


def total_vendido(pedidos):
    """Retorna la suma de los pedidos entregados."""
    total = 0.0
    for pedido in pedidos:
        if pedido["estado"] == "Entregado":
            total += pedido["total"]
    return total
