"""
Módulo de inventario.

Los productos se guardan en un ARREGLO UNIDIMENSIONAL (lista de Python).
Cada posición de la lista es un producto representado con un diccionario:
    {"codigo": "P001", "nombre": "Teclado", "precio": 15.5, "stock": 20}
"""

from utilidades import leer_texto, leer_entero, leer_decimal, confirmar, titulo

STOCK_MINIMO = 5   # por debajo de este valor se muestra una alerta


def generar_codigo(productos):
    """Genera el siguiente código disponible (P001, P002, ...)."""
    mayor = 0
    for p in productos:
        numero = int(p["codigo"][1:])
        if numero > mayor:
            mayor = numero
    return f"P{mayor + 1:03d}"


def buscar_producto(productos, codigo):
    """
    Recorre el arreglo y retorna la POSICIÓN (índice) del producto con ese
    código, o -1 si no existe.
    """
    codigo = codigo.upper()
    for i in range(len(productos)):
        if productos[i]["codigo"] == codigo:
            return i
    return -1


def registrar_producto(productos):
    """Pide los datos de un producto nuevo y lo agrega al final del arreglo."""
    titulo("REGISTRAR PRODUCTO")
    nombre = leer_texto("Nombre del producto: ")
    precio = leer_decimal("Precio unitario ($): ", minimo=0.01)
    stock = leer_entero("Stock inicial: ", minimo=0)

    producto = {"codigo": generar_codigo(productos), "nombre": nombre,
                "precio": precio, "stock": stock}
    productos.append(producto)          # escritura en el arreglo
    print(f"  ✓ Producto {producto['codigo']} registrado correctamente.")


def mostrar_productos(productos):
    """Recorre el arreglo e imprime los productos en forma de tabla."""
    titulo("LISTADO DE PRODUCTOS")
    if len(productos) == 0:
        print("  No hay productos registrados.")
        return

    print(f"  {'Código':<7} {'Nombre':<22} {'Precio':>9} {'Stock':>6}")
    print("  " + "-" * 47)
    for p in productos:                 # iteración sobre el arreglo
        alerta = "  ⚠ stock bajo" if p["stock"] < STOCK_MINIMO else ""
        print(f"  {p['codigo']:<7} {p['nombre']:<22} ${p['precio']:>8.2f} {p['stock']:>6}{alerta}")
    print(f"\n  Total de productos: {len(productos)}")


def editar_producto(productos):
    """Modifica un producto. Si se presiona Enter, se mantiene el valor actual."""
    titulo("EDITAR PRODUCTO")
    i = buscar_producto(productos, leer_texto("Código del producto a editar: "))
    if i == -1:
        print("  ✗ No existe un producto con ese código.")
        return

    p = productos[i]                    # lectura por índice
    print(f"  Editando {p['codigo']} - {p['nombre']} (Enter = mantener valor)")
    nombre = leer_texto(f"Nombre [{p['nombre']}]: ", permitir_vacio=True)
    precio = leer_decimal(f"Precio [{p['precio']:.2f}]: ", minimo=0.01, permitir_vacio=True)
    stock = leer_entero(f"Stock [{p['stock']}]: ", minimo=0, permitir_vacio=True)

    if nombre:
        p["nombre"] = nombre
    if precio is not None:
        p["precio"] = precio
    if stock is not None:
        p["stock"] = stock
    print("  ✓ Producto actualizado.")


def eliminar_producto(productos, pedidos):
    """
    Elimina un producto del arreglo.
    No se permite eliminarlo si tiene pedidos pendientes, para no dejar
    pedidos que apunten a un producto inexistente.
    """
    titulo("ELIMINAR PRODUCTO")
    i = buscar_producto(productos, leer_texto("Código del producto a eliminar: "))
    if i == -1:
        print("  ✗ No existe un producto con ese código.")
        return

    codigo = productos[i]["codigo"]
    for pedido in pedidos:
        if pedido["codigo_producto"] == codigo and pedido["estado"] == "Pendiente":
            print(f"  ✗ No se puede eliminar: el pedido {pedido['numero']} está pendiente con este producto.")
            return

    if confirmar(f"¿Seguro que desea eliminar {codigo} - {productos[i]['nombre']}?"):
        eliminado = productos.pop(i)    # eliminación por índice
        print(f"  ✓ Producto {eliminado['codigo']} eliminado.")
    else:
        print("  Operación cancelada.")


def valor_total_inventario(productos):
    """Retorna el valor total del inventario (precio × stock de cada producto)."""
    total = 0.0
    for p in productos:
        total += p["precio"] * p["stock"]
    return total
