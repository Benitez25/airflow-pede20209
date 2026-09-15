# Tarea Clase 4 - Celery Executor y Concurrencia

En esta tarea se desarrollaron 4 ejercicios relacionados con concurrencia en Apache Airflow, uso de workers, colas, pools, retries y Celery Canvas.

## Ejercicio 1 - Workers y concurrencia

Se creó un DAG con 6 tareas independientes, una por cada ciudad:

- Lima
- Arequipa
- Trujillo
- Chiclayo
- Piura
- Cusco

Cada tarea simula una ejecución de 10 segundos.

### Resultados

| Configuración | Tiempo |
|---|---:|
| 1 worker / concurrency 1 | 64.2 s |
| 1 worker / concurrency 6 | 14.8 s |
| 2 workers / concurrency 3 | 15.6 s |

Con una sola concurrencia, las tareas se ejecutan prácticamente una después de otra.

En los otros dos casos la capacidad total es de 6 tareas concurrentes, por eso los tiempos son parecidos. La diferencia es que en el último caso el trabajo se distribuye entre dos workers.

## Ejercicio 2 - Cola dedicada y Pool

Para este ejercicio se utilizó un escenario de procesamiento de información SAP.

Los procesos prioritarios fueron:

- Validación de documentos contables
- Validación del maestro de proveedores

Estos procesos se enviaron a una cola dedicada llamada `prioridad_sap`.

También se creó el Pool `sap_api_pool` con 2 slots.

Se eligieron 2 slots para limitar la cantidad de procesos que pueden usar el mismo recurso externo al mismo tiempo.

La cola permite separar los procesos prioritarios y el Pool ayuda a evitar saturar el recurso compartido.

Comando utilizado:

`airflow pools set sap_api_pool 2 "API SAP - máximo 2 procesos simultáneos"`

## Ejercicio 3 - Retries y Backoff

Se creó un DAG con una tarea que simula una llamada a una API externa con un 60% de probabilidad de falla.

La configuración utilizada fue:

- `retries=4`
- `retry_delay=7 segundos`
- `retry_exponential_backoff=True`
- `max_retry_delay=45 segundos`

Comportamiento observado:

- Intento 1: error
- Espera aproximada: 7 segundos
- Intento 2: error
- Espera aproximada: 14 segundos
- Intento 3: error
- Espera aproximada: 28 segundos
- Intento 4: ejecución correcta

En Airflow los reintentos se configuran directamente en la tarea. En Java, usando Quartz o Spring Batch, y en .NET con Hangfire, también se puede implementar este comportamiento, pero normalmente se requiere configurar de forma más explícita la política de reintentos, el manejo de errores y los tiempos de espera.

Airflow simplifica este proceso porque los intentos y errores quedan registrados directamente en los logs y en la interfaz del DAG.

## Ejercicio 4 - Celery Canvas

Para este ejercicio se eligió la opción A: Celery Canvas.

Se utilizó Celery de forma independiente a Airflow con Redis como broker.

Se probaron las siguientes funciones:

- `chain()` para ejecutar tareas de forma secuencial.
- `group()` para ejecutar varias tareas en paralelo.
- `chord()` para ejecutar una tarea final cuando termina un grupo.

Resultados obtenidos:

- Chain: `2500`
- Group: `[4, 9, 8, 15]`
- Chord: suma total `36`

## Estructura del proyecto

tarea_clase4/
- README.md
- ejercicio1/
- ejercicio2/
- ejercicio3/
- ejercicio4/

Cada carpeta contiene el código correspondiente a cada ejercicio.
