from airflow.decorators import dag, task
from datetime import datetime
import time

CIUDADES = ["Lima", "Arequipa", "Trujillo", "Chiclayo", "Piura", "Cusco"]


@dag(
    dag_id="reportes_ciudades_concurrencia",
    schedule=None,
    start_date=datetime(2026, 9, 1),
    catchup=False,
    tags=["clase4", "celery", "concurrencia"],
)
def reportes_ciudades_concurrencia():

    @task
    def generar_reporte(ciudad: str):
        inicio = time.time()
        print(f"Iniciando reporte de {ciudad}")
        time.sleep(10)
        duracion = time.time() - inicio
        print(f"Reporte de {ciudad} finalizado en {duracion:.2f} segundos")
        return ciudad

    # Se crean 6 tareas independientes, una por ciudad.
    for ciudad in CIUDADES:
        generar_reporte.override(task_id=f"reporte_{ciudad.lower()}")(ciudad)


reportes_ciudades_concurrencia()
