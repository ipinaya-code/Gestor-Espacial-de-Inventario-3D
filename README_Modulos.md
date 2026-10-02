# Mood Module: modulos, vision y proyeccion

Este documento describe que partes ya existen en Mood Module, cuales estan en desarrollo conceptual y que herramientas conviene evaluar para evolucionarlo como plataforma educativa 3D disponible para usuarios.

**Estado de referencia:** la implementacion existente en el repositorio al 2 de octubre de 2026. Las capacidades marcadas como propuestas no deben interpretarse como funciones terminadas.

## 1. Idea principal

Mood Module busca ser una plataforma educativa, dinamica y modular para crear y manipular objetos tridimensionales.

- **Mood** representa el estado, el ambiente y la experiencia de uso. La interfaz y la ayuda deberian adaptarse al contexto y al nivel del usuario.
- **Module** representa un sistema compuesto por capacidades separables: escena 3D, modelado, aprendizaje guiado, asistente, proyectos y otras que se agreguen con el tiempo.

La meta es que el usuario pueda explicar lo que quiere hacer en lenguaje natural, sin tener que aprender primero cada herramienta. Un agente podria convertir esa intencion en operaciones controladas sobre la escena y explicar los conceptos matematicos o geometricos implicados. GeoGebra y Blender sirven como referencias de interaccion y manipulacion visual, no como una afirmacion de que Mood Module ya tenga todas sus capacidades.

Ejemplos de la experiencia objetivo:

- «Crea un cubo en el origen»: crear el objeto en `(0, 0, 0)` y explicar el origen y los ejes.
- «Rota el objeto 2 45 grados sobre Y»: identificar el objeto, el eje y el angulo; ejecutar la rotacion y explicar el resultado.
- «Convierte el objeto 2 en un triangulo»: si no esta claro si se refiere a una figura plana, un prisma triangular o una piramide, pedir aclaracion antes de cambiar la escena.

## 2. Estado de los modulos

| Modulo                             | Estado                          | Implementacion o alcance actual                                                                                   |
| ---------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Interfaz web                       | Implementado                    | HTML, CSS y JavaScript con modulos ES; formulario de creacion, paneles y barra de atajos.                         |
| Escena 3D                          | Implementado                    | Three.js, camara perspectiva, luces, cuadricula, seleccion, OrbitControls y TransformControls.                    |
| Gestion de objetos                 | Implementado con alcance basico | Crear cubos, elegir color, seleccionar, mover, rotar, escalar y eliminar desde teclado o controles.               |
| API de objetos                     | Implementado                    | FastAPI expone salud, creacion, listado por espacio, actualizacion y eliminacion.                                 |
| Capas de backend                   | Implementado                    | Separacion entre rutas/esquemas, casos de uso, repositorio y modelo SQLModel.                                     |
| Persistencia local                 | Implementado con limitaciones   | SQLite guarda objetos y los campos admitidos por el modelo. La conexion permite configurar `DATABASE_URL`.        |
| Sesion y tema                      | Implementado                    | Los objetos de la sesion se restauran con `sessionStorage`; la preferencia de tema se conserva en `localStorage`. |
| Interfaz adaptable                 | Implementado                    | Barra de atajos horizontal y centrada en escritorio; compacta a la izquierda en celular.                          |
| Despliegue                         | Configurado                     | `render.yaml` define un servicio web en Render con SQLite en un disco persistente.                                |
| Documentacion y diagramas          | Implementado                    | Guias de arquitectura, API, base de datos, despliegue y plan manual de pruebas, ademas de diagramas PNG.          |
| Agente conversacional              | Propuesto                       | No hay chat, interpretacion de lenguaje natural ni ejecucion de herramientas por IA.                              |
| Explicacion pedagogica automatica  | Propuesto                       | El sistema aun no genera explicaciones sobre las operaciones ni adapta el contenido al nivel.                     |
| Formas distintas del cubo          | Propuesto                       | No existe aun un catalogo de primitivas o generacion de mallas arbitrarias desde instrucciones.                   |
| Usuarios, proyectos y colaboracion | Propuesto                       | No se implementan cuentas, propiedad de proyectos, enlaces compartidos ni edicion multiusuario.                   |

### Limites actuales importantes

- La escena ofrece rotacion y escala visuales, pero el `PUT` actual solo persiste nombre, posicion, color y `space_id`. Rotacion, escala y dimensiones no se guardan al actualizar.
- La API tiene un endpoint para listar por espacio, pero el frontend actual restaura la escena desde `sessionStorage`; no carga automaticamente el inventario desde ese endpoint al iniciar.
- Las pruebas documentadas en `tests/README_pruebas.md` son un plan manual. No equivalen a una suite automatizada completa.
- El acceso multiusuario, la autenticacion y los permisos por propietario aun no forman parte de las rutas actuales.

## 3. Modulos que se pueden implementar

### A. Asistente de intenciones 3D

**Objetivo:** traducir instrucciones del usuario a acciones estructuradas y validadas.

Responsabilidades futuras:

- Detectar la accion: crear, seleccionar, trasladar, rotar, escalar, cambiar forma o eliminar.
- Resolver la referencia del objeto por nombre o identificador visible.
- Extraer parametros, unidades y sistemas de coordenadas.
- Preguntar cuando falte informacion o haya mas de una interpretacion razonable.
- Mostrar que accion se va a realizar y permitir cancelarla o corregirla.

No conviene permitir que el modelo genere o ejecute JavaScript libre. El agente debe solicitar operaciones de una lista permitida, con argumentos validados por el backend.

### B. Motor de acciones y transformaciones

**Objetivo:** centralizar las operaciones que la interfaz y el agente pueden pedir.

Acciones iniciales sugeridas: `create_primitive`, `set_position`, `rotate_object`, `scale_object`, `set_color`, `delete_object` y `select_object`. Cada accion deberia validar el objeto, las unidades, los limites y el espacio de trabajo antes de modificar la escena.

Una capa comun de acciones evita que el agente implemente una logica diferente a la de los controles manuales.

### C. Biblioteca de geometria

**Objetivo:** ampliar el cubo actual con primitivas y formas educativas.

Orden sugerido: cubo/caja, esfera, cilindro, cono, plano y triangulo 2D; luego prisma triangular, piramide y formas parametrizadas. Distinguir explicitamente figuras 2D de solidos 3D.

### D. Explicacion y aprendizaje guiado

**Objetivo:** explicar las operaciones despues de realizarlas y ofrecer ayuda gradual.

Posibles funciones: explicacion paso a paso, modo de pistas, glosario de coordenadas y transformaciones, nivel principiante/intermedio, ejercicios guiados y preguntas de comprobacion. La explicacion debe basarse en los parametros realmente aplicados, no inventar lo que ocurrio.

### E. Historial, deshacer y rehacer

**Objetivo:** hacer segura la experimentacion.

Registrar cada accion como una operacion reversible; ofrecer deshacer/rehacer, vista previa de transformaciones y restauracion de versiones. Las eliminaciones y cambios destructivos deberian poder recuperarse.

### F. Proyectos, cuentas y espacios de trabajo

**Objetivo:** guardar y organizar el trabajo de cada usuario.

Incluir cuentas, proyectos, escenas, permisos y exportacion/importacion. Antes de multiusuario se necesita asociar cada registro a un propietario y validar autorizacion en cada endpoint.

### G. Compartir y comunidad

**Objetivo:** facilitar el uso educativo en grupos y redes.

Empezar con enlaces de solo lectura a proyectos y plantillas verificadas. Mas adelante evaluar galerias, comentarios, clases y colaboracion en tiempo real. No publicar escenas privadas por defecto.

### H. Exportacion e importacion 3D

**Objetivo:** permitir continuar el trabajo en otras herramientas.

Evaluar GLB/glTF para intercambio de escenas y STL para impresion 3D. Three.js ofrece exportadores para formatos comunes; validar materiales, unidades, nombres y permisos antes de habilitarlos.

### I. Accesibilidad, movil e idiomas

**Objetivo:** reducir barreras para distintos usuarios y dispositivos.

Mejorar controles tactiles, navegacion por teclado, etiquetas accesibles, contraste, mensajes de error y soporte multilingue. Probar dispositivos reales de bajo rendimiento, no solo emulacion de escritorio.

### J. Seguridad, calidad y operacion

**Objetivo:** hacer sostenible el acceso publico.

Autenticacion, permisos, limites de uso, validacion de entradas, control de costos de IA, registros sin datos sensibles, copias de seguridad, monitoreo y respuesta a errores. Establecer politica de privacidad y explicar que datos se envian al proveedor de IA.

## 4. Herramientas recomendadas

La recomendacion es evolucionar sobre la base actual y agregar herramientas cuando resuelvan una necesidad concreta, no reescribir toda la aplicacion desde el inicio.

| Area                | Recomendacion                                                                                                                                                                                                       | Cuando usarla                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Escena 3D           | Mantener Three.js y sus controles actuales.                                                                                                                                                                         | Adecuado para la escena y el editor 3D que ya existen.                            |
| Primitivas          | Geometrias nativas de Three.js; evaluar una libreria CSG solo si se requieren operaciones booleanas entre solidos.                                                                                                  | Primero construir primitivas simples y validar su uso educativo.                  |
| Frontend            | Mantener HTML/CSS/JavaScript modular para el MVP. Evaluar TypeScript y Vite cuando crezcan los modulos y el numero de desarrolladores.                                                                              | No es necesario migrar a React solo para incorporar un panel de chat.             |
| API                 | Mantener FastAPI, Pydantic y casos de uso; definir contratos tipados para cada accion.                                                                                                                              | Validar los argumentos del usuario y del agente en el servidor.                   |
| Agente IA           | Integrar el proveedor desde el backend mediante una interfaz propia y herramientas/function calling con esquemas Pydantic. Evaluar OpenAI, Anthropic, Gemini u Ollama segun costo, privacidad y calidad en español. | Probar primero un conjunto pequeño de intenciones; no enviar claves al navegador. |
| Datos locales       | Mantener SQLite para desarrollo y prototipos de una sola instancia.                                                                                                                                                 | Rapido y simple en local.                                                         |
| Datos publicos      | Migrar a PostgreSQL administrado y agregar migraciones con Alembic antes de ofrecer proyectos multiusuario.                                                                                                         | Mejor para concurrencia, copias y despliegues con crecimiento.                    |
| Autenticacion       | Evaluar Supabase Auth o autenticacion integrada en FastAPI; seleccionar una sola estrategia.                                                                                                                        | Antes de guardar proyectos privados de varios usuarios.                           |
| Pruebas backend     | `pytest` y `httpx` para endpoints, validadores y casos de uso.                                                                                                                                                      | Automatizar los flujos criticos del API.                                          |
| Pruebas de interfaz | Playwright para crear, transformar, usar el agente y validar escritorio/celular.                                                                                                                                    | Ejecutar en CI y antes de publicar versiones.                                     |
| Calidad             | Ruff para lint/formato de Python; GitHub Actions para ejecutar pruebas al integrar cambios.                                                                                                                         | Mantener calidad consistente al crecer el equipo.                                 |
| Despliegue          | Conservar Render para un piloto si su costo y disco persistente son adecuados; comparar PostgreSQL administrado antes de escalar.                                                                                   | Evitar SQLite efimero en plataformas sin disco persistente.                       |
| Monitoreo           | Logs estructurados y una herramienta como Sentry, con filtrado de informacion sensible.                                                                                                                             | Detectar fallos reales sin registrar conversaciones privadas innecesarias.        |

### Reglas para integrar IA con seguridad

1. Mantener las claves de proveedores solo en variables secretas del backend.
2. Hacer que el modelo proponga una accion estructurada; el backend valida identidad, permisos, tipos y rangos antes de ejecutarla.
3. No permitir SQL, Python, JavaScript o comandos arbitrarios generados por el modelo.
4. Pedir aclaracion para objetos ambiguos, figuras 2D/3D o unidades no especificadas.
5. Solicitar confirmacion para acciones destructivas y ofrecer deshacer cuando exista historial.
6. Separar los datos de la escena del contenido enviado a un proveedor externo y documentar la politica de retencion.
7. Registrar la accion validada y su resultado sin guardar secretos ni contenido sensible por defecto.

## 5. Proyeccion recomendada

### Fase 0: preparar un piloto publico

- Restringir CORS a los dominios reales y agregar autenticacion antes de aceptar datos de usuarios.
- Sacar la URL de produccion fija del cliente y manejar configuracion por entorno.
- Confirmar persistencia, backups y restauracion de la base de datos.
- Añadir pruebas automatizadas para CRUD, validacion y despliegue.
- Publicar primero con un grupo pequeno, terminos de uso y canal para reportar problemas.

### Fase 1: consolidar el editor

- Corregir la persistencia para que la escena recupere proyectos desde la API.
- Definir si rotacion, escala y dimensiones seran campos persistentes.
- Implementar historial y deshacer/rehacer.
- Añadir primitivas 3D y pruebas de escritorio y celular.

### Fase 2: agente educativo inicial

- Empezar con un conjunto reducido de comandos para crear, mover, rotar y cambiar color.
- Convertir lenguaje natural a acciones tipadas y mostrar una vista previa o resumen antes de ejecutar.
- Explicar coordenadas, ejes, angulos y unidades usando el resultado real de la operacion.
- Medir errores de interpretacion, latencia, costo y utilidad pedagogica con usuarios piloto.

### Fase 3: cuentas y proyectos

- Usar PostgreSQL, migraciones, autenticacion, propiedad de datos y permisos.
- Incorporar guardado/carga por proyecto, exportacion y enlaces compartidos con permisos explicitos.
- Añadir limites por usuario y controles de abuso.

### Fase 4: aprendizaje y comunidad

- Crear lecciones, ejercicios, pistas y niveles.
- Incorporar formas mas complejas, plantillas y espacios de trabajo compartidos.
- Evaluar colaboracion en tiempo real solo despues de validar el uso individual y la arquitectura de datos.

## 6. Requisitos antes de anunciarlo en redes

El repositorio tiene configuracion de despliegue para Render, pero eso por si solo no significa que la aplicacion este lista para una apertura amplia. Antes de invitar al publico:

- agregar autenticacion y permisos; las rutas actuales no muestran control de usuario;
- restringir CORS, que actualmente esta configurado para aceptar cualquier origen;
- confirmar que SQLite usa almacenamiento persistente y que hay backups recuperables;
- evitar que datos de usuarios queden en un espacio compartido sin separacion por propietario;
- definir privacidad, retencion de conversaciones, limites y costos si se conecta IA;
- probar carga, errores de red, celulares reales, accesibilidad y recuperacion;
- explicar que partes son experimentales y ofrecer contacto para soporte.

## 7. Enlaces del proyecto

- [README general](README.md)
- [Documentacion y diagramas](docs/README_documentacion.md)
- [Arquitectura actual y propuesta futura](docs/arquitectura/README_arquitectura.md)
- [Plan de pruebas](tests/README_pruebas.md)
- [Configuracion de base de datos](database/README_base_datos.md)
- [Despliegue](deploy/README_despliegue.md)
