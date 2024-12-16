import pandas as pd



class Missing_value_remover():
    def __init__(self) -> None:
        self.df = pd.read_csv('data/clean_data_with_mv.csv')
        self.mv_to_zero = {'garden':0, 'furnished':0, 'land_area':0}


    def remove_mv_for_living_area(self):
        mv_f_livare_df = self.df[self.df.living_area.isna()]
        for i in range(len(mv_f_livare_df.values)):
            entre = mv_f_livare_df.iloc[i]
            if len(self.df[self.df.number_of_rooms == entre.number_of_rooms].living_area)>1:
                mediana = self.df[self.df.number_of_rooms == entre.number_of_rooms].living_area.median()
            else:
                pre_med = self.df.living_area.sum()/self.df.number_of_rooms.sum()
                mediana = pre_med*entre.number_of_rooms
            cur_property_index = self.df.property_id == entre.property_id
            self.df.loc[cur_property_index,'living_area'] = mediana

    def remove_mv_for_terrace_surface(self):
        mv_f_ts_df = self.df[self.df.terrace_surface.isna()]
        counter = 0
        for i in range(len(mv_f_ts_df)):
            entre = mv_f_ts_df.iloc[i]
            interval_la_ts= self.df[(entre.living_area-20 <= self.df.living_area)&(self.df.living_area <= entre.living_area+20)&(self.df.terrace_surface>0)].terrace_surface
            if len(interval_la_ts) >1:
                mediana = interval_la_ts.median()
            else:
                new_interval = self.df[(entre.living_area-100 <= self.df.living_area)&(self.df.living_area <= entre.living_area+100)&(self.df.terrace_surface>0)].terrace_surface
                if len(new_interval) > 1:
                    mediana = new_interval.median()
                else:
                    new_interval =  self.df[(entre.living_area-300 <= self.df.living_area)&(self.df.living_area <= entre.living_area+300)&(self.df.terrace_surface>0)].terrace_surface
                    if len(new_interval)>1:
                        mediana = new_interval.median()
                    else:
                        counter+=1
            cur_property_index = self.df.property_id == entre.property_id
            self.df.loc[cur_property_index,'terrace_surface'] = mediana

    def set_mv_to_zero(self):
        self.df = self.df.fillna(value=self.mv_to_zero)

    def remove_mv_for_facades(self):
        mv_f_f_df = self.df[self.df.facades.isna()]
        counter = 0
        for i in range (len(mv_f_f_df)):
            entre = mv_f_f_df.iloc[i]
            condition = self.df[(self.df.number_of_rooms == entre.number_of_rooms)&(self.df.facades > 0)&(self.df.swimming_pool==entre.swimming_pool)]
            if len(condition) > 1:
                mode_1 = condition.facades.mode()[0]
            else:
                counter+=1
            cur_property_index = self.df.property_id == entre.property_id
            self.df.loc[cur_property_index,'facades'] = mode_1

    def set_unknown_cat_for_categorical(self):
        self.df = self.df.fillna(value={'state_of_building':'UNKNOWN', 'equipped_kitchen':'UNKNOWN'})

    def save_to_csv(self,path:str = 'data/clean_data_no_mv.csv'):
        self.df.to_csv(path)

    def remov_all_missing_values(self):
        self.remove_mv_for_living_area()
        self.remove_mv_for_terrace_surface()
        self.remove_mv_for_facades()
        self.set_mv_to_zero()
        self.set_unknown_cat_for_categorical()
        self.save_to_csv()
