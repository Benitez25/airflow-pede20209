# Ejercicio 4 - Opción A: Celery Canvas

Elegí **Celery Canvas**. Se usa Celery de forma independiente de Airflow y Redis como broker/backend.

El script `canvas_demo.py` prueba:

- `chain()`: tareas ejecutadas en secuencia.
- `group()`: tareas independientes ejecutadas en paralelo.
- `chord()`: un grupo paralelo seguido de un callback con todos los resultados.

## Ejecución

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

docker run -d --name redis-clase4 -p 6379:6379 redis:7-alpine

celery -A canvas_demo worker --loglevel=INFO --pool=solo
```

En otra terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python .\canvas_demo.py
```

## Resultado de referencia

```text
=== CHAIN ===
Resultado chain: 2500

=== GROUP ===
Resultado group: [4, 9, 8, 15]

=== CHORD ===
Resultado chord: {'resultados': [4, 9, 8, 15], 'suma_total': 36}
```

Se adjunta `evidencia_simulada.txt` como registro de referencia de la ejecución esperada.
