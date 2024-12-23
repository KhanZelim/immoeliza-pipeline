import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


# Load the data
file_path =  'D:\\BeCode\\Projects\\immoeliza-pipeline\\ml\\data\\base_clean_data_with_mv.csv' 


def plot_average_prices(file_path, save_dir):
    
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

file_path = 'D:\\BeCode\\Projects\\immoeliza-pipeline\\ml\\data\\base_clean_data_with_mv.csv'
save_dir = 'D:\\BeCode\\Projects\\immoeliza-pipeline\\analysis_immoeliza\\images'  
plot_average_prices(file_path, save_dir)