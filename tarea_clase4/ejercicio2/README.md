# Ejercicio 2 - Cola dedicada + Pool

## Escenario

El caso elegido es un proceso de datos SAP con 4 procesos independientes:

1. Validación de documentos contables.
2. Validación del maestro de proveedores.
3. Validación del maestro de materiales.
4. Generación de reporte de calidad.

Los dos primeros son prioritarios porque sus resultados se usan antes en validaciones financieras y de proveedores. Por eso se envían a la cola `prioridad_sap`, atendida por un worker dedicado.

Los cuatro procesos consultan una misma API SAP. Para evitar saturarla se usa el Pool `sap_api_pool` con **2 slots**, porque se asume que la API soporta de forma estable hasta dos consultas pesadas al mismo tiempo. Con 1 slot se perdería capacidad y con 4 ya no existiría protección.

## Crear el Pool

```powershell
docker compose exec airflow-scheduler airflow pools set sap_api_pool 2 "API SAP: maximo 2 consultas simultaneas"
```

## Worker de la cola prioritaria

El delta está en `docker-compose.delta.yml`. Se agrega dentro de `services:` y luego:

```powershell
docker compose up -d --force-recreate airflow-worker-prioridad-sap
```

La cola y el Pool cumplen funciones distintas: la cola decide qué worker recibe los procesos prioritarios y el Pool limita cuántas tareas pueden usar al mismo tiempo el recurso compartido.
