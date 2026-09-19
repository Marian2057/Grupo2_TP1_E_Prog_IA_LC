# Registro de uso de IA - TP1

Se utilizó IA como asistencia durante el desarrollo, siguiendo la metodología de
"Explicar, Planificar y Modificar". A continuación se documentan los tres prompts
más relevantes.

---

### Prompt 1 — Explicar

**Prompt:** "Tengo una lista de diccionarios con ventas (producto, categoría, precio,
cantidad). ¿Cómo calculo con pandas el producto más vendido y los ingresos totales por
categoría, sin usar bucles for manuales?"

- **Objetivo:** entender cómo reemplazar recorridos manuales por operaciones vectorizadas
  de pandas (`groupby`, `sum`, `idxmax`).
- **Propuesta de la IA:** convertir la lista en un `DataFrame` y usar
  `df.groupby("producto")["cantidad"].sum().idxmax()` para el producto líder, y
  `df.groupby("categoria")["total_venta"].sum()` para los ingresos por categoría.
- **Decisión:** se **aceptó** la propuesta tal cual, porque es exactamente la abstracción
  que pide la consigna en lugar de bucles manuales. Se integró en la función
  `calcular_indicadores()` de `funciones.py`.

---

### Prompt 2 — Planificar

**Prompt:** "Quiero organizar mi programa en dos módulos: uno con el menú y la interacción
con el usuario, y otro con las funciones de lógica (validar, guardar, buscar, calcular,
graficar). ¿Qué funciones debería tener cada módulo para que main.py quede simple?"

- **Objetivo:** planificar la separación de responsabilidades entre `main.py` y
  `funciones.py` antes de escribir el código.
- **Propuesta de la IA:** dejar en `funciones.py` toda la lógica pura (carga/guardado,
  validación, búsqueda, filtrado, cálculo de indicadores y gráfico) con anotaciones de
  tipo, y que `main.py` solo contenga el menú y las llamadas a esas funciones.
- **Decisión:** se **aceptó** la estructura general, pero se **modificó** agregando además
  una función de importación desde CSV (`importar_desde_csv`) que la IA no había sugerido,
  para cubrir el requisito de "fuente de datos externa" de la consigna.

---

### Prompt 3 — Modificar

**Prompt:** "Escribí una función que valide precio y cantidad ingresados por input(),
usando try/except, y que rechace valores negativos o texto no numérico sin cortar el
programa."

- **Objetivo:** implementar el manejo de errores exigido por la consigna de forma robusta.
- **Propuesta de la IA:** usar `try/except ValueError` alrededor de las conversiones
  `float()` e `int()`, devolviendo `None` cuando falla la conversión o cuando el valor es
  menor o igual a cero.
- **Decisión:** se **aceptó** la lógica central, pero se **modificó** para además validar
  que `producto` y `categoria` no estén vacíos, y se reutilizó la misma función tanto para
  la carga manual por consola como para la importación desde CSV, evitando duplicar código.

---

## Comprobación del funcionamiento

En los tres casos, el código propuesto se probó ejecutando `main.py` con datos válidos e
inválidos (texto en vez de números, precios negativos, campos vacíos) y revisando que
`ventas.json` reflejara correctamente los cambios. El detalle de las pruebas realizadas
está en la sección "Cómo se comprobó que el código funciona" del `README.md`.
