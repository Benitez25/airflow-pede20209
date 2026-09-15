from airflow.decorators import dag, task
from airflow.exceptions import AirflowException
from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)


@dag(
    dag_id="api_inestable_backoff",
    schedule=None,
    start_date=datetime(2026, 9, 1),
    catchup=False,
    tags=["clase4", "retries", "backoff"],
)
def api_inestable_backoff():

    @task(
        retries=4,
        retry_delay=timedelta(seconds=7),
        retry_exponential_backoff=True,
        max_retry_delay=timedelta(seconds=45),
    )
    def consultar_api_externa():
        valor = random.random()
        logger.info("Intento de llamada a API. random=%.4f", valor)

        if valor < 0.60:
            raise AirflowException("La API no estuvo disponible temporalmente")

        logger.info("Llamada a API completada correctamente")
        return {"estado": "ok", "random": valor}

    consultar_api_externa()


api_inestable_backoff()
