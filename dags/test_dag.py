from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_world():
    print("Hola desde Airflow!")

with DAG(
    dag_id='test_dag',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['test'],
) as dag:

    tarea = PythonOperator(
        task_id='saludo',
        python_callable=hello_world
    )
