# Registro de uso de IA - TP1

Se utilizó IA como asistencia durante el desarrollo, siguiendo la metodología de
"Explicar, Planificar y Modificar". A continuación se documentan los prompts más
relevantes y decisivos del proyecto, incluyendo la revisión final, la validación de
robustez y las pruebas de regresión.

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

### Prompt 4 — Revisión de requisitos y cobertura funcional

**Prompt:** "Revisá el proyecto completo y evaluá si cumple con los requisitos solicitados
por la consigna. Identificá si hay faltantes funcionales, y en caso de que no los haya,
confirmá el estado general del trabajo antes de continuar con mejoras."

- **Objetivo:** validar el cumplimiento de la consigna y detectar gaps funcionales antes de
  continuar con refuerzos de robustez.
- **Análisis de la IA:** el programa ya cumplía con la base funcional esperada, pero se
  identificaron mejoras necesarias en validación, manejo de errores y casos límite para que la
  aplicación fuera más sólida y segura.
- **Decisión:** se **tomó** como criterio de trabajo que no era necesario agregar nuevas
  funcionalidades de negocio, sino priorizar la corrección y reforzamiento de la lógica ya
  existente.

---

### Prompt 5 — Mejoras de robustez

**Prompt:** "Quiero que hagas todas las mejoras de prioridad alta: rechazar números no
finitos, validar la estructura al cargar el JSON, manejar errores al guardar y validar el
CSV antes de importarlo."

- **Objetivo:** fortalecer la estabilidad del programa ante entradas corruptas o inválidas.
- **Respuesta de la IA:** recomendar cambios en `funciones.py` para validar finitud de
  valores, estructura de `ventas.json`, manejo de excepciones en guardado, y validación de
  columnas/filas del CSV.
- **Decisión:** se **implementó** la validación reforzada y se dejó la lógica de persistencia
  segura ante errores sin mutar el estado en memoria si el guardado fallaba.

---

### Prompt 6 — Pruebas de regresión y corrección de bugs

**Prompt:** "Revisá los cambios del commit de 'Modificar venta' y hacé pruebas regresivas completas del proyecto. Si encontrás bugs, corregilos."

- **Objetivo:** garantizar que la funcionalidad nueva no rompa el resto del sistema.
- **Respuesta de la IA:** se detectaron problemas en la lógica de modificación y eliminación
  cuando la operación fallaba al guardar; el estado en memoria quedaba inconsistente.
- **Decisión:** se **corregió** para operar sobre copias temporales y persistir solo si el
  guardado final era exitoso, evitando estados parciales o corruptos.

---

### Prompt 7 — Validación del flujo interactivo completo

**Prompt:** "Antes de aceptar los cambios, ejecutá el flujo interactivo completo del
programa para verificar que no haya errores y que todo funcione correctamente."

- **Objetivo:** validar la experiencia de usuario real, no solo funciones aisladas.
- **Respuesta de la IA:** se ejecutó el menú principal con datos válidos e inválidos, y se
  comprobó que el comportamiento del flujo era consistente, incluso frente a errores de
  entrada y guardado.
- **Decisión:** se **aceptó** solo cuando el flujo interactivo quedó estable y sin errores de
  ejecución.

---

### Prompt 8 — Documentación final y preparación para PR

**Prompt:** "Quiero resumir todo lo hecho, dejarlo documentado y preparar una descripción
final de Pull Request con los cambios clave y el estado verificado."

- **Objetivo:** cerrar la entrega con documentación clara y un resumen técnico útil.
- **Respuesta de la IA:** se preparó un resumen de mejoras, validaciones, casos borde y
  pendientes no críticos, además de dejar el registro de prompts y el estado del README.
- **Decisión:** se **aceptó** la documentación final como soporte del trabajo terminado y de
  la revisión del proyecto.

---

## Comprobación del funcionamiento

En los distintos casos del proyecto, el código propuesto se probó ejecutando `main.py`
con datos válidos, inválidos, vacíos y de borde, revisando que `ventas.json` y los
indicadores reflejaran correctamente cada cambio. Además, se validaron los flujos de
modificación, eliminación, importación CSV y manejo de errores, para dejar la aplicación
más robusta y estable. El detalle de las pruebas realizadas está en la sección "Cómo se
comprobó que el código funciona" del `README.md`.
