from airflow.decorators import dag, task
from datetime import datetime
import random
import time

POOL = "sap_api_pool"
COLA_PRIORITARIA = "prioridad_sap"


@dag(
    dag_id="procesamiento_sap_prioridades_pool",
    schedule=None,
    start_date=datetime(2026, 9, 1),
    catchup=False,
    tags=["clase4", "colas", "pools"],
)
def procesamiento_sap_prioridades_pool():

    def consultar_api(nombre: str):
        print(f"[{nombre}] consultando API SAP")
        time.sleep(8)
        registros = random.randint(500, 3000)
        print(f"[{nombre}] finalizado - {registros} registros")
        return registros

    @task(queue=COLA_PRIORITARIA, pool=POOL, priority_weight=20)
    def validar_documentos_contables():
        return consultar_api("Documentos contables")

    @task(queue=COLA_PRIORITARIA, pool=POOL, priority_weight=20)
    def validar_proveedores():
        return consultar_api("Maestro de proveedores")

    @task(pool=POOL, priority_weight=5)
    def validar_materiales():
        return consultar_api("Maestro de materiales")

    @task(pool=POOL, priority_weight=1)
    def reporte_calidad():
        return consultar_api("Reporte de calidad")

    validar_documentos_contables()
    validar_proveedores()
    validar_materiales()
    reporte_calidad()


procesamiento_sap_prioridades_pool()
