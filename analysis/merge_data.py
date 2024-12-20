import pandas as pd
from datetime import datetime
from pandas.api.types import is_numeric_dtype
import numpy as np
import os


def clean_data(df):
    
    if df.isnull().sum().sum() != 0:
        # Replace empty strings with NaN
        df.replace('', np.nan, inplace=True)
        
        df.fillna(value=np.nan, inplace=True)

    # Columns that are expected to be numeric
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


def combine_data(file_name = None):
    base_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ml/data/base_clean_data_with_mv.csv')
    current_datetime = datetime.now().strftime("%d.%m.%Y")
    if file_name:
        extra_file =   os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../scraper/data/{file_name}')
    else:
        extra_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../scraper/data/row_properties_{current_datetime}.csv')
    # extra_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scraper/data/row_properties_17.12.2024.csv')
    # Check if the extra file exists
    if not os.path.exists(extra_file):
        print(f"Error: The file {extra_file} does not exist.")
        return None
    base_data = pd.read_csv(base_file)
    extra_data = pd.read_csv(extra_file)
    extra_data = clean_data(extra_data)

    # Combine the two datasets
    combined_data = pd.concat([base_data, extra_data], ignore_index=True)

    return combined_data 

 

def merge_data(file_name = None):
    combined_data = combine_data(file_name=file_name)
    if combined_data is None:
        return  
    
    # path to the ml/data folder
    cleaned_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml', 'data', 'base_clean_data_with_mv.csv')
    cleaned_dir = os.path.dirname(cleaned_filepath)

    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)  

    combined_data.to_csv(cleaned_filepath, index=False)
    print(f"Data has been successfully combined, cleaned, and saved to {cleaned_filepath}")



