# Infraestructura y despliegue

Esta carpeta concentra la documentación y referencias relacionadas con el entorno operativo del proyecto.

## Punto de verdad del despliegue

La configuración principal de Render está en la raíz del repositorio:

- [../render.yaml](../render.yaml)

## Archivos relacionados

- [../docker](../docker): contenedorización del backend/frontend.
- [../database](../database): conexión y persistencia de la base de datos.

## Objetivo

- Servir la aplicación web con FastAPI.
- Exponer la API y el frontend desde un único servicio.
- Gestionar datos persistentes para SQLite en entorno de despliegue.
