from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow import DAG
import os
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
import seaborn as sns
import matplotlib.pyplot as plt

# Function to combine data
def combine_data():
    base_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scraper/data/base_row_properties.csv')
    extra_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scraper/data/row_properties_18.12.2024.csv')

    if not os.path.exists(extra_file):
        raise FileNotFoundError(f"Error: The file {extra_file} does not exist.")
    
    base_data = pd.read_csv(base_file)
    extra_data = pd.read_csv(extra_file)

    combined_data = pd.concat([base_data, extra_data], ignore_index=True)

    return combined_data

# Function to clean data
def clean_data(df):
    if df.isnull().sum().sum() != 0:
        df.replace('', np.nan, inplace=True)
        df.fillna(value=np.nan, inplace=True)

    numeric_columns_df = df[["property_id", "living_area", "price", "number_of_rooms", "postal_code",
                             "terrace_surface", "garden", "land_area", "facades", "open_fire", "swimming_pool", "furnished"]]
    
    numeric_columns = df.select_dtypes(include=np.number).columns
    is_all_numeric = len(numeric_columns) == len(numeric_columns_df.columns)

    if not is_all_numeric:
        convert_dict = {}
        for column in numeric_columns_df:
            columnSeriesObj = numeric_columns_df[column]
            if is_numeric_dtype(columnSeriesObj.dtype):
                convert_dict[column] = columnSeriesObj.dtype
            else:
                convert_dict[column] = np.float64  
        
        df = df.astype(convert_dict)

    return df

# Function to save cleaned data
def save_cleaned_data(df):
    cleaned_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml', 'data', 'base_clean_data_with_mv.csv')
    cleaned_dir = os.path.dirname(cleaned_filepath)

    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)

    df.to_csv(cleaned_filepath, index=False)
    print(f"Data has been successfully combined, cleaned, and saved to {cleaned_filepath}")

# Function to plot house price distribution
def house_distribution():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml', 'data', 'base_clean_data_with_mv.csv')
    df = pd.read_csv(file_path)

    sns.set_theme(style="whitegrid", palette="muted")

    plt.figure(figsize=(10, 6))
    ax = sns.histplot(df['price'], kde=True, color='skyblue', bins=30, edgecolor='black')

    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.xticks(ticks=range(0, 10000000, 1000000), labels=[f'${i}M' for i in range(0, 10)])

    plt.title("Distribution of House Prices", fontsize=18, fontweight='bold', pad=20, color='navy')
    plt.xlabel('Price (in Millions Euro)', fontsize=14, labelpad=10, color='darkslategray')
    plt.ylabel('Number of Houses', fontsize=14, labelpad=10, color='darkslategray')

    for line in ax.lines:
        line.set_color('blue') 
        line.set_linewidth(2)   

    sns.despine(left=True, bottom=False)

    # Check if the images folder exists, if not, create it
    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..', 'analysis', 'images')
 
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    image_path = os.path.join(images_folder, 'house_price_distribution_new.png')


    plt.tight_layout()
    plt.savefig(image_path)

    print(f"Plot saved to {image_path}")

# Default arguments for the DAG
default_args = {
    'owner': 'veena',
    'start_date': days_ago(1),
    'retries': 3,
}

# DAG definition
dag = DAG(
    'data_processing_dag',
    default_args=default_args,
    description='DAG for combining, cleaning, and saving data',
    schedule_interval='@daily',  
)

# Task to combine data
combine_task = PythonOperator(
    task_id='combine_data',
    python_callable=combine_data,
    dag=dag,
)

# Task to clean data
def clean_data_task(**kwargs):
    df = kwargs['task_instance'].xcom_pull(task_ids='combine_data')
    return clean_data(df)

clean_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data_task,
    provide_context=True,
    dag=dag,
)

# Task to save cleaned data
def save_cleaned_data_task(**kwargs):
    df = kwargs['task_instance'].xcom_pull(task_ids='clean_data')
    save_cleaned_data(df)

save_task = PythonOperator(
    task_id='save_cleaned_data',
    python_callable=save_cleaned_data_task,
    provide_context=True,
    dag=dag,
)

# Task to plot house price distribution
plot_task = PythonOperator(
    task_id='house_distribution',
    python_callable=house_distribution,
    dag=dag,
)

# Set task dependencies
combine_task >> clean_task >> save_task >> plot_task

