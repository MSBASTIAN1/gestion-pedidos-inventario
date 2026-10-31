"""
Funciones de apoyo para la entrada de datos.
Validan lo que escribe el usuario para que el programa no se caiga si
ingresa letras donde se espera un número, o deja un campo vacío.
"""


def leer_texto(mensaje, permitir_vacio=False):
    """Lee un texto. Si permitir_vacio es False, insiste hasta que no esté vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto or permitir_vacio:
            return texto
        print("  ✗ Este campo no puede estar vacío.")


def leer_entero(mensaje, minimo=0, permitir_vacio=False):
    """
    Lee un número entero mayor o igual a 'minimo'.
    Si permitir_vacio es True y el usuario presiona Enter, retorna None
    (se usa al editar para "mantener el valor actual").
    """
    while True:
        texto = input(mensaje).strip()
        if texto == "" and permitir_vacio:
            return None
        if texto.isdigit() and int(texto) >= minimo:
            return int(texto)
        print(f"  ✗ Ingrese un número entero mayor o igual a {minimo}.")


def leer_decimal(mensaje, minimo=0.0, permitir_vacio=False):
    """Lee un número decimal (acepta coma o punto) mayor o igual a 'minimo'."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        if texto == "" and permitir_vacio:
            return None
        try:
            valor = float(texto)
            if valor >= minimo:
                return round(valor, 2)
        except ValueError:
            pass
        print(f"  ✗ Ingrese un número mayor o igual a {minimo}.")


def confirmar(mensaje):
    """Pregunta s/n y retorna True si la respuesta es 's'."""
    return input(f"{mensaje} (s/n): ").strip().lower() == "s"


def titulo(texto):
    """Imprime un título con formato."""
    print("\n" + "=" * 60)
    print(f" {texto}")
    print("=" * 60)
