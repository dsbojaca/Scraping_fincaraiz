from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow import DAG 
import pendulum
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from etl.extract import extract_properties
from etl.transform import clean_data
from etl.load import load_to_postgres
from utils.driver import get_driver



def extract_task():
    driver = get_driver()
    return extract_properties(driver)

def clean_task(ti):
    raw_data = ti.xcom_pull(task_ids='extract')
    return clean_data(raw_data)

def load_task(ti):
    cleaned_data = ti.xcom_pull(task_ids='transform')
    load_to_postgres(cleaned_data)


default_args = {
    'owner': 'David',
    'start_date': pendulum.datetime(2025, 1, 1, tz="America/Bogota"),
    'retries': 1
}

with DAG(
    dag_id='etl_fincaraiz_dag',
    default_args= default_args,
    schedule='@daily',  # o '@hourly', '0 6 * * *', etc.
    catchup=False,
    tags=['fincaraiz', 'etl'],
) as dag:
    
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_task
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=clean_task
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_task
    )

    extract >> transform >> load