from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scraper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ml')))

from scraper.src.pipeline import Pipeline
from ml.utils.creator import Creator

default_args = {
    'owner': 'Ihor',
    'retries': 3,
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=2),
}

def collect_extra_links(pipeline):
    pipeline.colect_extra_links()

def scrap_data(pipeline):
    return pipeline.scrap_data()

def prepare_data(pipeline):
    pipeline.prepare_data()

def save_to_csv(pipeline):
    current_datetime = datetime.now().strftime("%d.%m.%Y")
    filepath = f'row_properties_{current_datetime}.csv'
    pipeline.save_to_csv(filepath)

def train_model():
    creator = Creator()
    creator.create_models()

with DAG(
    dag_id='retrain_models_2',
    default_args=default_args,
    description='Rescrape data, cleans it up, trains model and saves updated model.',
    start_date=datetime(2024, 12, 17),
    schedule_interval='@daily',
) as dag:
    pipeline = Pipeline()

    task1 = PythonOperator(
        task_id='collect_extra_links',
        python_callable=collect_extra_links,
        op_args=[pipeline],
    )
    task2 = PythonOperator(
        task_id='scrap_data',
        python_callable=scrap_data,
        op_args=[pipeline],
    )
    task3 = PythonOperator(
        task_id='prepare_data',
        python_callable=prepare_data,
        op_args=[pipeline],
    )
    task4 = PythonOperator(
        task_id='save_to_csv',
        python_callable=save_to_csv,
        op_args=[pipeline],
    )
    task5 = PythonOperator(
        task_id='create_model',
        python_callable=train_model,
    )

    task1 >> task2 >> task3 >> task4 >> task5
