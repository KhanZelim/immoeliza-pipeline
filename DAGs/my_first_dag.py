from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scraper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ml')))



from scraper import main as scrape_extra_data
from ml import main as clean_data_and_create_models

default_args = {
    'owner' : 'Ihor',
    'retries':3,
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='retrain_models',
    default_args= default_args,
    description='Rescrape data, cleans it up, trains model and saves updated model. ',
    start_date=datetime(2024,12,17,2),
    schedule_interval='@daily',

) as dag:
    task1 = PythonOperator(
        task_id = 'scrape_extra_data',
        python_callable = scrape_extra_data,
    )
    task2 = PythonOperator(
        task_id= 'create_model',
        python_callable=  clean_data_and_create_models
    )
    task1 >> task2