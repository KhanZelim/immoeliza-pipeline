import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

class Categorical_encoder:
    def __init__(self,columns_to_onehot:list=['subtype_of_property','postal_code'],random_state:int=124) -> None:
        self.df = pd.read_csv('data/clean_data_no_outliers.csv')
        self.columns_to_onehot = columns_to_onehot
        self.df = self.df.dropna()
        self.X = None
        self.y = None
        self.X_train =None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.splited_list = {'train':self.X_train, 'test':self.X_test}

    def split_dataset(self,random_state:int=124):
        mask = self.df.number_of_rooms == 0
        self.df = self.df[~mask]
        self.X = self.df.drop('price',axis=1,inplace=False)
        self.y = self.df['price']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X,self.y,random_state=random_state)



    def kitchen_tipe_preprocessing(self):
        self.df.equipped_kitchen = self.df.apply(lambda x: x.equipped_kitchen.replace('USA_INSTALLED','INSTALLED'),axis = 1 )
        self.df.equipped_kitchen = self.df.apply(lambda x: x.equipped_kitchen.replace('USA_SEMI_EQUIPPED','SEMI_EQUIPPED'),axis = 1 )
        self.df.equipped_kitchen = self.df.apply(lambda x: x.equipped_kitchen.replace('USA_UNINSTALLED','NOT_INSTALLED'),axis = 1 )
        self.df.equipped_kitchen = self.df.apply(lambda x: x.equipped_kitchen.replace('USA_HYPER_EQUIPPED','HYPER_EQUIPPED'),axis = 1 )
    
   
   
    def kitchen_type_ordinal_encode(self):
        train_cat = self.X_train.equipped_kitchen.to_numpy().reshape(-1,1)
        test_cat = self.X_test.equipped_kitchen.to_numpy().reshape(-1,1)
        encoder = OrdinalEncoder(categories=[['NOT_INSTALLED','SEMI_EQUIPPED','UNKNOWN','INSTALLED','HYPER_EQUIPPED']]).fit(train_cat)
        self.X_train.equipped_kitchen = encoder.transform(train_cat)
        self.X_test.equipped_kitchen= encoder.transform(test_cat)
        

    def state_of_building_ordinal_encode(self):
        train_cat = self.X_train.state_of_building.to_numpy().reshape(-1,1)
        test_cat = self.X_test.state_of_building.to_numpy().reshape(-1,1)
        state_of_building_encoder = OrdinalEncoder(categories=[['TO_RESTORE','TO_RENOVATE','TO_BE_DONE_UP','UNKNOWN','JUST_RENOVATED','GOOD','AS_NEW']]).fit(train_cat)
        self.X_train.state_of_building = state_of_building_encoder.transform(train_cat)
        self.X_test.state_of_building = state_of_building_encoder.transform(test_cat)
    
    def custom_combiner(obj,feature,category,):
        return str(category)

    def column_one_hot_encode(self,column_name:str):
        train_cat = self.X_train[column_name].to_numpy().reshape(-1,1)
        test_cat = self.X_test[column_name].to_numpy().reshape(-1,1)
        encoder = OneHotEncoder(drop='first',feature_name_combiner=self.custom_combiner,sparse_output=False).fit(train_cat)
        train_a = encoder.transform(train_cat)
        test_a = encoder.transform(test_cat)
        train_cn = encoder.get_feature_names_out()
        train_df = pd.DataFrame(train_a,columns=train_cn)
        test_df = pd.DataFrame(test_a,columns=train_cn)
        self.X_train = self.X_train.reset_index(drop=True)
        self.X_test = self.X_test.reset_index(drop=True)
        train_df = train_df.reset_index(drop=True)
        test_df = test_df.reset_index(drop=True)
        self.X_train = self.X_train.join(train_df)
        self.X_train.drop([column_name],axis=1,inplace=True)
        self.X_test = self.X_test.join(test_df)
        self.X_test.drop([column_name],axis=1,inplace=True)


    def postal_code_preprocessing(self):
        test_df = self.df.groupby('postal_code').postal_code.value_counts()
        sum = 0
        to_small_pc_list=[]
        for i in range(len(test_df)):
            if test_df.iloc[i] < 5:
                sum+=test_df.iloc[i]
                to_small_pc_list.append(test_df.keys()[i])
        for i in to_small_pc_list:
            test_df = self.df[self.df.postal_code == i]
            for row in test_df.property_id:
                index = self.df.property_id == row
                self.df.loc[index,'postal_code'] = 9999
        

    def one_hot_all_columns(self):
        for column in self.columns_to_onehot:
            self.column_one_hot_encode(column)
            



    def save_to_csv(self):
        self.X_train.drop(['Unnamed: 0','facades','property_id','type_of_property'],axis=1,inplace=True)
        self.X_test.drop(['Unnamed: 0','facades','property_id','type_of_property'],axis=1,inplace=True)
        self.X_train.to_csv(f'data/encoded_X_train.csv')
        self.X_test.to_csv('data/encoded_X_test.csv')
        self.y_train.to_csv('data/encoded_y_train.csv')
        self.y_test.to_csv('data/encoded_y_test.csv')

    # def encode_df(self,df):
    #     # self.kitchen_type_ordinal_encode(df)
    #     # self.state_of_building_ordinal_encode(df)
    #     # self.postal_code_preprocessing()
    #     # self.one_hot_all_columns(df)
    #     # self.save_to_csv(df)
    
    def encode_df(self):
        self.postal_code_preprocessing()
        self.kitchen_tipe_preprocessing()
        self.split_dataset()
        self.kitchen_type_ordinal_encode()
        self.state_of_building_ordinal_encode()
        self.one_hot_all_columns()
        self.save_to_csv()
                