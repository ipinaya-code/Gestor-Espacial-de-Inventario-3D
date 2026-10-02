# Plan de pruebas del sistema

Esta carpeta está dedicada a la validación funcional, técnica y de comportamiento del proyecto Gestor Espacial de Inventario 3D.

## Objetivo

Verificar que el sistema:

- crea objetos 3D correctamente,
- guarda la información en la base de datos,
- elimina y actualiza registros sin errores,
- mantiene la experiencia visual y operativa en la escena 3D,
- responde adecuadamente a validaciones y errores del usuario.

---

## 1. Tipos de pruebas recomendadas

### 1.1. Pruebas de caja negra

Se validan comportamientos desde la perspectiva del usuario sin revisar el código interno.

#### Casos sugeridos

1. Crear un objeto con nombre válido.
2. Crear un objeto con posición por defecto.
3. Crear varios objetos en la misma sesión.
4. Seleccionar un objeto en la escena.
5. Mover, rotar y escalar un objeto con el gizmo.
6. Eliminar un objeto con la tecla `Z`.
7. Eliminar con `Delete` o `Backspace`.
8. Comprobar que el objeto desaparece tanto en la escena como en la base de datos.
9. Cambiar entre modo oscuro y claro.
10. Verificar que el cambio de tema no elimina los objetos ya creados.
11. En escritorio, verificar que la barra de atajos quede horizontal y centrada arriba.
12. En celular, verificar que la barra quede compacta a la izquierda y no se cruce con el boton de tema.

### 1.2. Pruebas de caja blanca

Se validan flujos internos, funciones y respuestas de la API.

#### Casos sugeridos

1. Verificar que `create_item()` crea un `ItemModel` correcto.
2. Validar que `get_all_by_space()` devuelve solo ítems del espacio indicado.
3. Comprobar que `delete()` elimina un registro existente y devuelve `True`.
4. Confirmar que `update()` modifica solo los campos permitidos.
5. Revisar que `ItemCreateSchema` rechaza nombres vacíos.
6. Probar validación de colores con formato hexadecimal incorrecto.
7. Validar que `position` y `dimensions` aceptan solo valores válidos.
8. Validar que la respuesta de la API tiene formato `JSON` correcto.

### 1.3. Pruebas de integración

Se validan las interacciones entre frontend, backend y base de datos.

#### Casos sugeridos

1. Crear un objeto desde la interfaz y verificar que se guarde en SQLite.
2. Recargar la página y comprobar que los objetos de la sesión siguen visibles.
3. Eliminar desde la interfaz y confirmar que se borra en la base de datos.
4. Mover un objeto desde la escena y verificar que se actualiza en la API.
5. Probar el flujo completo: crear → seleccionar → mover → guardar → eliminar.

### 1.4. Pruebas de regresión

Se ejecutan para asegurar que cambios nuevos no rompen funcionalidades ya validadas.

#### Casos sugeridos

1. Cambiar de modo claro/oscuro sin reiniciar la sesión.
2. Añadir varios objetos seguidos sin borrarse.
3. Verificar que la escena vacía no se rellena con objetos antiguos al abrir la app.
4. Confirmar que la API sigue respondiendo en `/health`.

---

## 2. Casos de prueba funcionales por módulo

### 2.1. Frontend / interfaz

- Abrir la app sin objetos creados.
- Crear un objeto desde el formulario.
- Validar que el campo de nombre no queda vacío.
- Validar que el botón de agregar se habilita de nuevo tras la petición.
- Cambiar el modo claro/oscuro.
- Ver que el menú de opciones no afecta la escena.

### 2.2. Escena 3D

- Alinear la cámara con `OrbitControls`.
- Seleccionar un cubo con clic.
- Ver el gizmo en el objeto correcto.
- Mover el cubo en cada eje.
- Rotar el cubo y comprobar el cambio visual.
- Escalar el cubo con la herramienta adecuada.

### 2.3. API Backend

- `GET /health` responde `200` y `status: ok`.
- `POST /api/v1/items/` crea un registro exitosamente.
- `GET /api/v1/items/space/{space_id}` retorna todos los objetos del espacio.
- `PUT /api/v1/items/{item_id}` actualiza los atributos persistibles.
- `DELETE /api/v1/items/{item_id}` elimina el registro y responde `204`.

### 2.4. Base de datos

- Se crea la tabla `spatial_items` correctamente al iniciar la app.
- Los registros se persisten con UUID.
- Los valores `x`, `y`, `z`, `width`, `height`, `depth` se almacenan con el tipo correcto.
- La base sigue funcionando aunque el frontend se recargue.

---

## 3. Matriz de pruebas recomendada

| Área        | Objetivo         | Resultado esperado               |
| ----------- | ---------------- | -------------------------------- |
| UI          | Crear objeto     | Un cubo aparece en la escena     |
| UI          | Cambiar tema     | Solo cambia la apariencia        |
| Frontend    | Selección        | Se activa el gizmo correctamente |
| Frontend    | Tecla Z          | El objeto se elimina             |
| API         | POST             | Código 201 y registro creado     |
| API         | GET              | Lista de objetos del espacio     |
| API         | DELETE           | Código 204 y registro borrado    |
| BD          | Persistencia     | Datos guardados en SQLite        |
| Integración | Crear + eliminar | Flujo completo sin errores       |

---

## 4. Casos de prueba críticos para este proyecto

1. Crear más de un cubo sin reiniciar la aplicación.
2. Eliminar un cubo y verificar que no queda en la base de datos.
3. No perder la sesión cuando cambia el tema.
4. No reiniciar la escena al insertar un elemento nuevo.
5. Validar que el modo claro/oscuro no rompe la lógica del inventario.
6. Probar el comportamiento con posiciones por defecto y personalizadas.
7. Verificar que el sistema conservaal menos la sesión actual en `sessionStorage`.

---

## 5. Criterios de aceptación

Se considera aceptado el sistema si cumple lo siguiente:

- Crear objetos es funcional.
- Eliminar objetos es funcional.
- La escena 3D refleja el estado real de la base de datos.
- El cambio de tema no altera la lógica del negocio.
- La API responde correctamente a las operaciones principales.
- Los datos persistentes quedan guardados en SQLite.

---

## 6. Sugerencia de ejecución

Se recomienda ejecutar pruebas en este orden:

1. Validación de la API (`/health`, crear, listar, borrar).
2. Validación del frontend con la escena 3D.
3. Validación de base de datos.
4. Pruebas de regresión con varios objetos.
5. Verificación final del flujo completo del sistema.

---

## 7. Conclusión

Este proyecto tiene un flujo claro para pruebas funcionales y de integración: desde la interfaz, pasando por la API y la base de datos, hasta la representación visual en 3D. La estrategia sugerida combina caja negra, caja blanca e integración para detectar tanto errores de negocio como errores técnicos.

## 8. Pruebas futuras del agente educativo

Estos casos son criterios para una etapa futura; el agente conversacional todavía no está implementado.

1. Solicitar «crea un cubo en el origen» y comprobar que se interpreta como posición `(0, 0, 0)` y que se explica el origen.
2. Pedir una rotación de un objeto identificado por número o nombre y validar objeto, eje, ángulo y unidad antes de ejecutarla.
3. Pedir «convierte el objeto en un triángulo» y confirmar que el agente solicita aclaración entre una figura 2D, un prisma triangular o una pirámide.
4. Dar una instrucción ambigua o imposible y verificar que el agente pregunta o informa la limitación en vez de cambiar un objeto incorrecto.
5. Revisar que la explicación posterior describa los conceptos geométricos y parámetros realmente aplicados.
6. Comprobar que las acciones persistibles usan la API existente y que la interfaz identifica claramente el objeto afectado.
