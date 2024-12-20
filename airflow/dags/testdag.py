import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Define the function from your script
def plot_average_prices():
    file_path = '/mnt/d/BeCode/Projects/immoeliza-pipeline/ml/data/base_clean_data_with_mv.csv'
    save_dir = '/mnt/d/BeCode/Projects/immoeliza-pipeline/analysis_immoeliza/images'

    # Load the data
    data = pd.read_csv(file_path)

    # Filter for houses and apartments
    filtered_data = data[data['type_of_property'].isin(['HOUSE', 'APARTMENT'])]

    # Calculate average price per postal code and property type
    average_prices = (
        filtered_data.groupby(['postal_code', 'type_of_property'])['price']
        .mean()
        .reset_index()
    )

    # Limit to top 20 postal codes with most listings
    top_postal_codes = filtered_data['postal_code'].value_counts().head(20).index
    average_prices = average_prices[average_prices['postal_code'].isin(top_postal_codes)]

    # Pivot the data for easier plotting
    pivot_data = average_prices.pivot(index='postal_code', columns='type_of_property', values='price')

    # Create the plot
    pivot_data.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'lightcoral'])
    plt.title('Average Prices of Houses and Apartments by Postal Code')
    plt.xlabel('Postal Code')
    plt.ylabel('Average Price (€)')
    plt.xticks(rotation=45)
    plt.legend(title='Property Type')
    plt.tight_layout()

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Save the plot
    save_path = os.path.join(save_dir, "average_prices_by_postal_code.png")
    plt.savefig(save_path)
    plt.close()

    print(f"Plot saved to {save_path}")


def house_distribution():
    file_path = '/mnt/d/BeCode/Projects/immoeliza-pipeline/ml/data/base_clean_data_with_mv.csv'
    save_dir = '/mnt/d/BeCode/Projects/immoeliza-pipeline/analysis_immoeliza/images'

    # Load the data
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
    plt.tight_layout()

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Save the plot
    save_path = os.path.join(save_dir, "house_price_distribution.png")
    plt.savefig(save_path)
    plt.close()

    print(f"Plot saved to {save_path}")
    


# Initialize the DAG
dag = DAG(
    dag_id="plot_average_prices_dag",
    start_date=datetime(2024, 12, 1),  # Adjust the start date
    schedule_interval=None,  # Set to None for manual execution
    catchup=False,  # Disable backfilling
)

# Define the PythonOperator
generate_plot_task = PythonOperator(
    task_id="generate_plot_task",
    python_callable=plot_average_prices,  # The function to execute
    dag=dag,
)

# Define the PythonOperator
generate_plot_task1 = PythonOperator(
    task_id="generate_plot_task1",
    python_callable=house_distribution,  # The function to execute
    dag=dag,
)

