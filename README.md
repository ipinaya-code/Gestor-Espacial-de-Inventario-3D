# Mood Module

Plataforma educativa interactiva para crear y manipular objetos en un espacio tridimensional. La experiencia actual funciona como un editor 3D de inventario; la vision del producto es evolucionar hacia un entorno modular asistido por un agente que ayude a aprender haciendo.

## Vision del producto

El nombre expresa dos ideas complementarias:

- **Mood** representa el estado, el ambiente y la experiencia de trabajo: la plataforma debe sentirse dinamica y adaptarse al contexto y al nivel del usuario.
- **Module** representa una plataforma compuesta por modulos que puedan crecer y asumir capacidades distintas, como modelado, aprendizaje guiado y automatizacion.

La interaccion toma como referencias los entornos visuales y de manipulacion 3D, como GeoGebra y Blender, pero el objetivo diferencial es que el usuario pueda expresar lo que quiere lograr en lenguaje natural sin tener que aprender primero todas las herramientas. Un agente interpretaria la intencion, ejecutaria acciones disponibles en la escena y explicaria los conceptos utilizados para que cada accion tambien sea una oportunidad de aprendizaje.

### Ejemplos de la experiencia objetivo

- «Crea un cubo en el origen»: crear el objeto en `(0, 0, 0)` y explicar que el origen es la interseccion de los ejes X, Y y Z.
- «Rota el objeto 2 45 grados sobre Y»: identificar el objeto, aplicar la rotacion alrededor del eje Y y explicar el angulo y el eje usados.
- «Convierte el objeto 2 en un triangulo»: si la peticion no determina una forma tridimensional concreta, preguntar si el usuario quiere un triangulo plano, un prisma triangular o una piramide antes de modificar el objeto.

El agente deberia privilegiar acciones comprensibles y reversibles: identificar claramente el objeto, confirmar o aclarar parametros ambiguos, ejecutar mediante operaciones permitidas y explicar el resultado en lenguaje accesible. La explicacion debe describir los conceptos y parametros aplicados, no presentar una respuesta opaca.

### Estado de la vision

La interfaz 3D, las operaciones basicas y la API descritas en este README corresponden al estado actual del proyecto. La conversacion en lenguaje natural, el agente de IA, la explicacion pedagogica automatica y la generacion de formas mas alla del cubo son objetivos futuros; aun no estan implementados.

## Para que sirve

El sistema permite:

- Crear varios objetos 3D desde un formulario.
- Ubicar cada objeto mediante coordenadas tridimensionales.
- Elegir un color para cada objeto.
- Seleccionar objetos directamente en la escena.
- Mover, rotar y escalar objetos seleccionados.
- Eliminar objetos con la tecla `Z`, `Delete` o `Backspace`.
- Guardar los objetos en una base de datos SQLite.
- Cambiar entre modo claro y modo oscuro sin afectar las operaciones del inventario.
- Usar la barra de opciones centrada en la parte superior en PC y compacta, alineada a la izquierda en celulares.

## Tecnologias utilizadas

### Frontend

- HTML5 y CSS3.
- JavaScript con modulos ES.
- Three.js para la escena 3D, la cuadricula, la camara y los controles.
- `OrbitControls` para mover la camara.
- `TransformControls` para mover, rotar y escalar objetos.

### Backend

- Python.
- FastAPI para crear la API REST.
- Uvicorn como servidor ASGI.
- SQLModel y SQLAlchemy para trabajar con los modelos y repositorios.
- SQLite como base de datos local.
- `aiosqlite` para acceso asincrono a SQLite.
- Pydantic para validar los datos recibidos por la API.

## Estructura del proyecto

```text
Gestor Espacial de Inventario 3D/
├── README.md
├── README_Modulos.md
├── render.yaml
├── requirements.txt
├── backend/
│   ├── main.py
│   ├── spatial_inventory.db
│   └── app/
│       ├── core/
│       │   └── database.py
│       ├── domain/
│       │   └── entities.py
│       ├── infrastructure/
│       │   ├── models.py
│       │   └── repositories.py
│       ├── presentation/
│       │   ├── routes.py
│       │   └── schemas.py
│       └── use_cases/
│           └── item_use_cases.py
└── frontend/
    ├── index.html
    ├── css/
    │   ├── main.css
    │   ├── base.css
    │   ├── components.css
    │   ├── panel.css
    │   ├── responsive.css
    │   └── variables.css
    └── js/
        ├── api.js
        ├── main.js
        ├── scene.js
        └── components/
            └── item3d.js
```

## Documentación

La documentación disponible del proyecto incluye:

- [Modulos implementados y propuestos, herramientas y hoja de ruta](README_Modulos.md)
- [Indice de documentación](docs/README_documentacion.md)
- [Arquitectura, endpoints y diagramas PNG](docs/arquitectura/README_arquitectura.md)
- [Plan de pruebas manuales](tests/README_pruebas.md)
- [Configuración de base de datos](database/README_base_datos.md)
- [Despliegue](deploy/README_despliegue.md)

## Organización del repositorio

El proyecto quedó organizado por capas para facilitar mantenimiento y despliegue:

```text
Gestor Espacial de Inventario 3D/
├── backend/
│   ├── main.py
│   ├── spatial_inventory.db
│   └── app/
│       ├── core/
│       ├── domain/
│       ├── infrastructure/
│       ├── presentation/
│       └── use_cases/
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
├── database/
│   ├── README_base_datos.md
│   └── connection.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── deploy/
│   └── README_despliegue.md
├── docs/
│   ├── README_documentacion.md
│   └── arquitectura/
│       ├── README_arquitectura.md
│       └── imagenes/
├── tests/
│   └── README_pruebas.md
├── README.md
├── README_Modulos.md
├── requirements.txt
├── render.yaml
└── .gitignore
```

### Responsabilidades por carpeta

- `backend/`: lógica de la API y servicios del sistema.
- `frontend/`: interface gráfica, Three.js y UX del inventario 3D.
- `database/`: conexión, sesión y configuración de la base de datos.
- `docker/`: contenedorización local del proyecto.
- `deploy/`: documentación y referencias de despliegue del proyecto.
- `docs/`: documentación técnica, arquitectura y diagramas.
- `tests/`: plan de pruebas, casos de validación y escenarios del sistema.

> La configuración activa de Render queda en [render.yaml](render.yaml) en la raíz del proyecto como única fuente de despliegue.

## Como funciona

1. El usuario completa el nombre, la posicion y el color del objeto.
2. El frontend envia los datos al backend mediante una peticion `POST`.
3. FastAPI valida la informacion recibida con Pydantic.
4. El repositorio crea un registro en la tabla `spatial_items` y lo guarda con `commit()`.
5. El backend devuelve el objeto creado con su identificador unico.
6. Three.js crea el cubo y lo agrega a la escena sin eliminar los objetos anteriores.
7. El objeto nuevo queda seleccionado para poder manipularlo inmediatamente.
8. Los objetos creados durante la sesion tambien se conservan en `sessionStorage`, para restaurarlos si el navegador recarga la pagina.
9. Al eliminarlo, el frontend envia una peticion `DELETE`; el backend borra el registro de SQLite y despues el frontend retira el cubo de la escena y de la sesion.
10. La barra de opciones muestra las acciones disponibles (`M`, `R`, `S`, `Z` y `Esc`) y tambien permite activarlas con clic.

La pagina inicia intencionalmente con la escena vacia. Los registros antiguos que existan en la base de datos no se dibujan automaticamente al abrir una sesion nueva. Los objetos creados durante la sesion se conservan en la escena y se restauran si el navegador recarga la pagina, evitando que desaparezcan al agregar otro objeto.

Si se deja la posicion inicial `(0, 0.5, 0)`, los objetos nuevos se colocan automaticamente en posiciones libres para evitar que queden superpuestos. Las coordenadas personalizadas se respetan.

El modo claro u oscuro solo cambia la apariencia de la interfaz, el fondo, la iluminacion y la cuadricula. La preferencia se conserva en `localStorage` y no modifica las operaciones del inventario.

## Controles

| Tecla                  | Accion                                                             |
| ---------------------- | ------------------------------------------------------------------ |
| `M`                    | Mover el objeto seleccionado                                       |
| `R`                    | Rotar el objeto seleccionado                                       |
| `S`                    | Escalar el objeto seleccionado                                     |
| `Z`                    | Eliminar el objeto seleccionado de la escena y de la base de datos |
| `Esc`                  | Deseleccionar el objeto                                            |
| `Delete` / `Backspace` | Eliminar el objeto seleccionado                                    |
| Arrastrar con el mouse | Mover la camara alrededor de la escena                             |

Los controles tambien se pueden pulsar desde la barra de opciones. En pantallas de escritorio esta barra se muestra centrada en la parte superior; en celulares se muestra compacta en el costado izquierdo, mientras el boton de tema permanece en la esquina superior derecha.

El editor permite mover, rotar y escalar los objetos en la escena. Actualmente, la API persiste el nombre, la posicion, el color y el espacio; la rotacion, la escala y las dimensiones no se guardan en la base de datos.

## Base de datos

La aplicacion utiliza SQLite y crea el archivo:

```text
backend/spatial_inventory.db
```

La tabla principal es `spatial_items`. Cada registro contiene:

- `id`: identificador UUID.
- `name`: nombre del objeto.
- `space_id`: espacio al que pertenece.
- `color`: color hexadecimal.
- `x`, `y`, `z`: posicion del objeto.
- `width`, `height`, `depth`: dimensiones del objeto.

La base de datos se inicializa automaticamente cuando se inicia FastAPI.

## Instalacion

Se recomienda utilizar Python 3.10 o una version posterior.

Desde la raiz del proyecto, crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```powershell
pip install -r requirements.txt
```

## Ejecucion del backend

Entra en la carpeta `backend` y ejecuta Uvicorn:

```powershell
cd backend
uvicorn main:app --reload --port 8000
```

La API estara disponible en:

```text
http://127.0.0.1:8000
```

Documentacion interactiva de FastAPI:

```text
http://127.0.0.1:8000/docs
```

Comprobacion de estado:

```text
http://127.0.0.1:8000/health
```

## Ejecucion del frontend

Abre `frontend/index.html` con Live Server desde VS Code o utiliza cualquier servidor estatico local. Por ejemplo, con Live Server la direccion suele ser:

```text
http://127.0.0.1:5500/frontend/index.html
```

Al usar Live Server local, el frontend se conecta al backend en `http://127.0.0.1:8000`. Si se abre desde el servicio Render, usa automaticamente el mismo dominio para la API.

## Despliegue en Render

El archivo `render.yaml` configura un servicio web unico que sirve el frontend y la API, y guarda SQLite en un disco persistente montado en `/var/data`. Para desplegarlo:

1. Sube los cambios a la rama `main` de GitHub.
2. En Render, crea un Blueprint y conecta el repositorio `Gestor-Espacial-de-Inventario-3D`.
3. Revisa el plan y los costos mostrados por Render antes de confirmar la creacion.
4. Al terminar el despliegue, abre el dominio `onrender.com` asignado al servicio.

El Blueprint usa un plan web pago y un disco persistente de 1 GB. Los servicios gratuitos de Render no admiten discos persistentes, por lo que no sirven para conservar SQLite de forma fiable entre reinicios y despliegues. La base alojada comienza vacia; los datos que solo esten en el archivo SQLite local no se copian automaticamente. El enlace publico no tiene autenticacion: cualquier persona que lo conozca puede crear o eliminar objetos.

## Endpoints principales

| Metodo   | Ruta                             | Funcion                                      |
| -------- | -------------------------------- | -------------------------------------------- |
| `GET`    | `/health`                        | Comprueba que la API esta activa.            |
| `POST`   | `/api/v1/items/`                 | Crea un objeto 3D.                           |
| `GET`    | `/api/v1/items/space/{space_id}` | Consulta los objetos de un espacio.          |
| `DELETE` | `/api/v1/items/{item_id}`        | Elimina un objeto por su UUID.               |
| `PUT`    | `/api/v1/items/{item_id}`        | Actualiza los datos persistibles del objeto. |

## Arquitectura del backend

El backend esta separado por responsabilidades:

- `core`: configuracion de la base de datos y sesiones.
- `domain`: entidades del dominio.
- `infrastructure`: modelos SQLModel y repositorios de persistencia.
- `use_cases`: reglas de negocio para crear, consultar y eliminar objetos.
- `presentation`: rutas HTTP y esquemas de validacion.

Este enfoque permite modificar la persistencia o la interfaz de la API sin mezclar toda la logica en un solo archivo.

## Estado del proyecto

El proyecto funciona como un prototipo de inventario espacial 3D. En local usa SQLite en `backend/spatial_inventory.db`; en Render puede conservar la base en su disco persistente. La rotacion y escala son visuales, mientras que el endpoint `PUT` persiste los campos admitidos por el modelo, incluida la posicion. Antes de compartir el enlace para uso publico, se recomienda agregar autenticacion y restringir CORS.
