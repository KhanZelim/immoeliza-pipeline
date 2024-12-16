import joblib

class Encoder():
    def __init__(self,data : dict = {}) -> None:
        self.df_for_prediction = joblib.load('data/empty_df.joblib')
        self.new_row = None
        self.user_row = data
        print(self.user_row)
        self.postal_code_set = set(self.df_for_prediction.keys()[32:])
        self.subtype_set = set(self.df_for_prediction.keys()[10:32])
    

    def entrie_encode(self):
        self.new_row = [0]*len(self.df_for_prediction.columns)
        self.df_for_prediction.loc[len(self.df_for_prediction)] = self.new_row
        self.df_for_prediction.loc[len(self.df_for_prediction)-1,['number_of_rooms','living_area','land_area',]] = self.user_row['number_of_rooms'],self.user_row['living_area'],self.user_row['land_area']
        self.df_for_prediction.loc[len(self.df_for_prediction)-1,['garden','terrace_surface','state_of_building','equipped_kitchen']] = self.user_row['garden'],self.user_row['terrace'],self.user_row['state_of_building'],self.user_row['equipped_kitchen']
        postal_code = str(self.user_row['postal_code'])

        if postal_code not in self.postal_code_set:
            if str(postal_code) != '1010':
                self.df_for_prediction.loc[len(self.df_for_prediction)-1,'9999'] = 1
        else:
            self.df_for_prediction.loc[len(self.df_for_prediction)-1,postal_code] = 1

        if self.user_row['subtype'] != 'APARTMENT':
            self.df_for_prediction.loc[len(self.df_for_prediction)-1,self.user_row['subtype']] = 1
        
        if self.user_row['open_fire']:
            self.df_for_prediction.loc[len(self.df_for_prediction)-1,'open_fire'] = 1
        if self.user_row['swiming_pool']:
            self.df_for_prediction.loc[len(self.df_for_prediction)-1,'swimming_pool'] = 1
        if self.user_row['furnished']:
            self.df_for_prediction.loc[len(self.df_for_prediction)-1,'furnished'] = 1
    
        return self.df_for_prediction, self.user_row['modelchoise']
    
    def csv_encode(self):
            pass
        
        
        
        
        
        
        # print(self.df_for_prediction.keys()[10:32]) subtype
        
#  modelchoise='XGB' 
# test_data = {
#     'num_of_room':4,
#     'postal_code':1020,
#     'subtype':'VILLA',
#     'living_area':159.0,
#     'land_area':10.0,
#     'garden':0.0,
#     'terrace':0.0, 
#     'open_fire':None,
#     'furnished':None,
#     'swiming_pool':None,
#     'state_of_building':5.0,
#     'equipped_kitchen':3.
# }


# e = Encoder(test_data)
# e.entrie_encode()