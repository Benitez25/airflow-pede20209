# Ejercicio 3 - Retries con backoff

La task simula una API que falla el 60% de las veces usando `random.random() < 0.60`.

Configuración:

```python
retries=4
retry_delay=timedelta(seconds=7)
retry_exponential_backoff=True
max_retry_delay=timedelta(seconds=45)
```

Elegí 7 segundos como espera inicial porque permite ver claramente el crecimiento sin hacer demasiado larga la prueba. Con backoff exponencial los intervalos crecen aproximadamente a 7, 14, 28 y hasta un máximo de 45 segundos.

## Evidencia

Se adjunta `evidencia_log_simulado.txt`. La corrida de referencia muestra tres fallos y luego éxito, con esperas de 7, 14 y 28 segundos.

## Comparación Java / .NET

En Java se podría resolver con **Quartz** o **Spring Batch**, pero parte de la lógica tendría que configurarse o programarse de forma explícita. Con Quartz habría que capturar la excepción del `Job`, decidir cuándo reprogramarlo, llevar el conteo de intentos y calcular la espera entre cada ejecución. Spring Batch tiene soporte de retry, pero igual se deben definir las excepciones reintentables, la política de reintentos y cómo se integra con el `Step`. En .NET, **Hangfire** incluye `AutomaticRetryAttribute`, aunque para una política específica de backoff, un tiempo máximo y reglas propias de error se tienen que configurar intervalos o filtros adicionales. En Airflow esta lógica queda separada de la función de negocio: `retries`, `retry_delay`, `retry_exponential_backoff=True` y `max_retry_delay` controlan el comportamiento desde la task. Además, Airflow guarda el estado de cada intento y deja el historial en la UI y los logs. Eso reduce código adicional y hace más simple revisar qué pasó cuando una llamada externa falla temporalmente.
