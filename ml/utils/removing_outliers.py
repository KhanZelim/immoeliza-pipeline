import pandas as pd


class Outlier_remover():
    def __init__(self,column_list : list = ['price','number_of_rooms','living_area','land_area']) -> None:
        self.df = pd.read_csv('data/clean_data_no_mv.csv')
        self.columns_to_be_droped = ['Unnamed: 0','Unnamed: 0.1','link','type_of_sale','postal_code_str','locality_name']
        self.columns_with_outliers = column_list
        self.df.drop(self.columns_to_be_droped,axis=1,inplace=True)

    def remove_outlier_for_column(self,column_name : str ):
        Q1 = self.df[column_name].quantile(0.25)
        Q3 = self.df[column_name].quantile(0.75)
        IQR = Q3-Q1
        threshold = 1.5
        outliers = self.df[(self.df[column_name]< Q1 - threshold * IQR)|(self.df[column_name] >  Q3 + threshold * IQR)&(self.df.subtype_of_property != 'CASTLE')]
        self.df = self.df.drop(outliers.index)

    def save_to_csv(self,path: str = 'data/clean_data_no_outliers.csv'):
       self.df.to_csv(path) 

    def remove_all_outliers(self):
        for column in self.columns_with_outliers:
            self.remove_outlier_for_column(column_name=column)
        self.save_to_csv()
