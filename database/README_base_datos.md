# Base de datos

Esta carpeta agrupa la parte de persistencia y la conexión a la base de datos del proyecto.

## Archivos principales

- [connection.py](connection.py): configuración del engine, sesión y acceso a SQLite.

## Estado actual

La aplicación usa SQLite como base de datos principal y el archivo real se mantiene en:

- [backend/spatial_inventory.db](../backend/spatial_inventory.db)

## Uso recomendado

- La conexión y la sesión de la base de datos deben vivir en esta carpeta para mantener la estructura limpia.
- La capa del backend usa este módulo desde [backend/app/core/database.py](../backend/app/core/database.py) como wrapper compatibilidad.
- En producción, la conexión puede sobrescribirse con la variable de entorno `DATABASE_URL`.
