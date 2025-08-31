# -*- coding: utf-8 -*-
"""
Sistema de pedidos para una hamburguesería
-------------------------------------------------
Funcionalidades:
  - Recibe pedidos.
  - Calcula total y vuelto.
  - Guarda cada venta en ventas.txt.
  - Registra entrada y salida de encargados en registro.txt.

Roles sugeridos para el equipo (comentarios útiles para asignación de tareas):
  - Programador/a Principal: Mantener funciones, validaciones y flujo del menú.
  - Diseñador/a de Menús: Ajustar MENSAJES y textos para claridad.
  - Gestor/a de Archivos: Verificar el formato de ventas.txt y registro.txt.
  - Tester: Probar entradas inválidas y flujos alternativos.
  - Documentador/a: Completar la documentación y capturas.
  - Coordinador/a: Planificar tareas, fechas y revisión final.
"""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from datetime import datetime
from pathlib import Path

# ---------- Configuración ----------
MONEDA = "ARS$"
VENTAS_FILE = "ventas.txt"
REGISTRO_FILE = "registro.txt"

# Menú editable por el "Diseñador/a de Menús"
MENU_ITEMS = [
    {"codigo": "H1", "nombre": "Hamburguesa Clásica", "precio": Decimal("3500.00")},
    {"codigo": "H2", "nombre": "Doble Queso", "precio": Decimal("4200.00")},
    {"codigo": "H3", "nombre": "Bacon", "precio": Decimal("4800.00")},
    {"codigo": "E1", "nombre": "Papas Fritas", "precio": Decimal("1500.00")},
    {"codigo": "B1", "nombre": "Gaseosa", "precio": Decimal("1200.00")},
    {"codigo": "B2", "nombre": "Agua", "precio": Decimal("1000.00")},
    {"codigo": "P1", "nombre": "Postre", "precio": Decimal("2000.00")},
]

# ---------- Utilidades ----------
def money(val: Decimal) -> str:
    return f"{MONEDA}{val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"

def now_str() -> str:
    # Formato claro para Argentina (AAAA-MM-DD HH:MM:SS)
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_files():
    # Crea archivos si no existen
    Path(VENTAS_FILE).touch(exist_ok=True)
    Path(REGISTRO_FILE).touch(exist_ok=True)

def leer_int(mensaje: str, minimo: int = None, maximo: int = None) -> int:
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print("⚠️  Debe ingresar un número.")
            continue
        if not dato.lstrip("-").isdigit():
            print("⚠️  Ingrese solo números enteros.")
            continue
        num = int(dato)
        if minimo is not None and num < minimo:
            print(f"⚠️  Debe ser >= {minimo}.")
            continue
        if maximo is not None and num > maximo:
            print(f"⚠️  Debe ser <= {maximo}.")
            continue
        return num

def leer_decimal(mensaje: str) -> Decimal:
    while True:
        s = input(mensaje).strip().replace(",", ".")
        try:
            return Decimal(s)
        except (InvalidOperation, ValueError):
            print("⚠️  Importe inválido. Ej: 10000 o 10000.50")

# ---------- Registro de turnos ----------
current_operator = None

def registrar_entrada():
    global current_operator
    if current_operator:
        print(f"Ya hay un encargado en turno: {current_operator}. Finalice su turno antes de iniciar otro.")
        return
    nombre = input("Nombre del encargado/a: ").strip()
    if not nombre:
        print("⚠️  El nombre no puede estar vacío.")
        return
    current_operator = nombre
    linea = f"[{now_str()}] ENTRADA - Encargado: {nombre}\n"
    with open(REGISTRO_FILE, "a", encoding="utf-8") as f:
        f.write(linea)
    print("✅ Entrada registrada.")

def registrar_salida():
    global current_operator
    if not current_operator:
        print("⚠️  No hay encargado/a en turno.")
        return
    nombre = current_operator
    current_operator = None
    linea = f"[{now_str()}] SALIDA  - Encargado: {nombre}\n"
    with open(REGISTRO_FILE, "a", encoding="utf-8") as f:
        f.write(linea)
    print("✅ Salida registrada.")

# ---------- Ventas ----------
def mostrar_menu_items():
    print("\n=== MENÚ ===")
    for i, it in enumerate(MENU_ITEMS, start=1):
        print(f"{i:>2}. {it['nombre']:<22} {money(it['precio'])}  (cód: {it['codigo']})")
    print("  0. Terminar pedido")

def tomar_pedido():
    if not current_operator:
        print("⚠️  Debe registrar ENTRADA antes de tomar pedidos.")
        return
    pedido = []
    while True:
        mostrar_menu_items()
        eleccion = leer_int("Elija un ítem por número (0 para terminar): ", minimo=0, maximo=len(MENU_ITEMS))
        if eleccion == 0:
            break
        item = MENU_ITEMS[eleccion - 1]
        cant = leer_int(f"Cantidad para '{item['nombre']}': ", minimo=1, maximo=50)
        pedido.append({"codigo": item["codigo"], "nombre": item["nombre"], "precio": item["precio"], "cantidad": cant})

    if not pedido:
        print("Pedido vacío. No se registró venta.")
        return

    subtotal = sum(it["precio"] * it["cantidad"] for it in pedido)
    print(f"Subtotal: {money(subtotal)}")

    # Cobro
    pago = leer_decimal("Importe recibido: ")
    while pago < subtotal:
        print(f"⚠️  El pago es menor que el total ({money(subtotal)}).")
        pago = leer_decimal("Importe recibido: ")
    vuelto = (pago - subtotal)

    # Guardar venta
    venta_id = calcular_proximo_id()
    guardar_venta(venta_id, current_operator, pedido, subtotal, pago, vuelto)

    # Ticket en pantalla
    imprimir_ticket(venta_id, current_operator, pedido, subtotal, pago, vuelto)

def calcular_proximo_id() -> int:
    # Cuenta cuántas ventas hay registradas en el archivo
    try:
        with open(VENTAS_FILE, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.startswith("--- Venta #")) + 1
    except FileNotFoundError:
        return 1

def guardar_venta(venta_id: int, encargado: str, items: list, total: Decimal, pago: Decimal, vuelto: Decimal):
    with open(VENTAS_FILE, "a", encoding="utf-8") as f:
        f.write(f"--- Venta #{venta_id:04d} - {now_str()} - Encargado: {encargado}\n")
        for it in items:
            linea = f"  {it['codigo']} {it['nombre']} x{it['cantidad']} = {money(it['precio'] * it['cantidad'])}\n"
            f.write(linea)
        f.write(f"  TOTAL:  {money(total)}\n")
        f.write(f"  PAGO:   {money(pago)}\n")
        f.write(f"  VUELTO: {money(vuelto)}\n")
        f.write("-" * 46 + "\n")

def imprimir_ticket(venta_id: int, encargado: str, items: list, total: Decimal, pago: Decimal, vuelto: Decimal):
    print("\n" + "=" * 32)
    print(f"Ticket - Venta #{venta_id:04d}")
    print(f"Fecha: {now_str()}")
    print(f"Encargado/a: {encargado}")
    print("-" * 32)
    for it in items:
        print(f"{it['nombre']} x{it['cantidad']:>2} -> {money(it['precio'] * it['cantidad'])}")
    print("-" * 32)
    print(f"TOTAL : {money(total)}")
    print(f"PAGO  : {money(pago)}")
    print(f"VUELTO: {money(vuelto)}")
    print("=" * 32 + "\n")

def ver_archivo(path: str, titulo: str):
    print(f"\n=== {titulo} ===")
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if contenido:
                print(contenido)
            else:
                print("(vacío)")
    except FileNotFoundError:
        print("(no existe)")

# ---------- Menú principal ----------
def main():
    ensure_files()
    print("🍔 Bienvenid@ al Sistema de Pedidos - Hamburguesería")
    while True:
        print("\nMenú principal:")
        print(" 1) Registrar ENTRADA")
        print(" 2) Registrar SALIDA")
        print(" 3) Tomar pedido")
        print(" 4) Ver ventas.txt")
        print(" 5) Ver registro.txt")
        print(" 0) Salir")
        op = leer_int("Opción: ", minimo=0, maximo=5)
        if op == 1:
            registrar_entrada()
        elif op == 2:
            registrar_salida()
        elif op == 3:
            tomar_pedido()
        elif op == 4:
            ver_archivo(VENTAS_FILE, "ventas.txt")
        elif op == 5:
            ver_archivo(REGISTRO_FILE, "registro.txt")
        elif op == 0:
            print("¡Gracias! Hasta luego.")
            break

if __name__ == "__main__":
    main()
