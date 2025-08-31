# Sistema de Pedidos - Hamburguesería

## Integrantes y Roles
- Nombre 1 — Programador/a Principal
- Nombre 2 — Diseñador/a de Menús
- Nombre 3 — Gestor/a de Archivos
- Nombre 4 — Tester
- Nombre 5 — Documentador/a
- Nombre 6 — Coordinador/a

> Editar con los nombres reales del equipo (máx. 6).

---
## Descripción breve del sistema
Aplicación en Python (modo consola) para gestionar pedidos de una hamburguesería.
Permite:
- Registrar entrada/salida de encargados (registro.txt).
- Tomar pedidos con un menú editable.
- Calcular total y vuelto con precisión de 2 decimales.
- Guardar cada venta en ventas.txt con detalle de ítems y totales.

**Archivos generados**
- `ventas.txt`: cada venta se agrega al final con fecha/hora, encargado e ítems.
- `registro.txt`: log de ENTRADA/SALIDA de encargados.

---
## Cómo ejecutar
1. Instalar Python 3.10+
2. Descargar `sistema_pedidos.py` y colocarlo en una carpeta vacía.
3. Abrir una terminal en esa carpeta y correr:
   ```bash
   python sistema_pedidos.py
   ```
4. Flujo recomendado para la demo:
   - Opción 1: Registrar ENTRADA (ingresar nombre).
   - Opción 3: Tomar pedido (elegir ítems y cantidades, cobrar).
   - Opción 4/5: Ver los archivos generados.
   - Opción 2: Registrar SALIDA.

> **Tip**: El archivo `MENU_ITEMS` dentro del código se puede editar para cambiar precios y nombres.

---
## Capturas de pantalla (pegar aquí)
- **Captura 1:** Menú principal visible.
- **Captura 2:** Registro de ENTRADA.
- **Captura 3:** Pedido con selección de ítems.
- **Captura 4:** Ticket impreso y archivos vistos.

---
## Pruebas sugeridas (para el Tester)
- Pago menor al total → el sistema debe pedir un nuevo importe.
- Pedido vacío → no debe guardar venta.
- Entrada doble sin salida → el sistema debe avisar.
- Cantidad inválida (texto o < 1) → debe rechazar y volver a pedir.

---
## Estructura interna (resumen para el Programador/a)
- `registrar_entrada()` / `registrar_salida()` → escribe en `registro.txt`.
- `tomar_pedido()` → loop de selección, cálculo, cobro y guardado.
- `guardar_venta()` → agrega una venta formateada a `ventas.txt`.
- `calcular_proximo_id()` → numera las ventas.
- `MENU_ITEMS` → lista de productos editable.

---
## Buenas prácticas
- Usar nombres claros de archivos y mantener todo en una sola carpeta.
- Probar antes de entregar (distintos flujos y errores de entrada).
- Guardar un backup de `ventas.txt` y `registro.txt` si hacen muchas pruebas.
