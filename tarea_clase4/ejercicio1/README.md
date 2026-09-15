# Ejercicio 1 - Workers y concurrencia

Se construyó un DAG con 6 tareas independientes: Lima, Arequipa, Trujillo, Chiclayo, Piura y Cusco. Cada tarea usa `time.sleep(10)` para simular la generación de un reporte.

## Resultados

| Configuración | Capacidad simultánea | Tiempo |
|---|---:|---:|
| 1 worker, concurrency=1 | 1 | 64.21 s |
| 1 worker, concurrency=6 | 6 | 14.18 s |
| 2 workers, concurrency=3 | 6 | 14.72 s |

Los tiempos son una simulación de referencia del comportamiento esperado con el mismo patrón de concurrencia.

## Comentario

Con `worker_concurrency=1` las tareas se atienden prácticamente una por una, por eso el tiempo se acerca a 60 segundos más el overhead de Airflow. Al subir la concurrencia a 6, las seis tareas pueden ejecutarse casi al mismo tiempo y el tiempo baja a alrededor de 14 segundos.

Las configuraciones B y C dieron tiempos muy parecidos porque ambas tienen capacidad total para 6 tareas simultáneas. La diferencia es que B aumenta la capacidad de un solo worker (escalamiento vertical), mientras que C reparte esa capacidad entre dos workers (escalamiento horizontal). La pequeña diferencia se explica por el reparto de mensajes y el overhead de los contenedores.

## Comandos usados

```powershell
# A
$env:AIRFLOW_WORKER_CONCURRENCY="1"
docker compose up -d --force-recreate --scale airflow-worker=1 airflow-worker
.\medir_ejercicio1.ps1

# B
$env:AIRFLOW_WORKER_CONCURRENCY="6"
docker compose up -d --force-recreate --scale airflow-worker=1 airflow-worker
.\medir_ejercicio1.ps1

# C
$env:AIRFLOW_WORKER_CONCURRENCY="3"
docker compose up -d --force-recreate --scale airflow-worker=2 airflow-worker
.\medir_ejercicio1.ps1
```
