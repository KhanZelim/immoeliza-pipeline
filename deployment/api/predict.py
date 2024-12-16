from  api.user_data_validation import Encoder
import joblib
import xgboost


class Predictor:
    def __init__(self,flag = 0,form_data : dict = {}) -> None:
        self.user_data_encoder = Encoder(form_data)
        if flag == 1:
            self.df_to_predict = self.user_data_encoder.csv_encode()
        else:
            self.df_to_predict,self.model_name = self.user_data_encoder.entrie_encode()
        self.linear = joblib.load('data/models/linear_regression_model.joblib')
        self.xgboost = xgboost.XGBRegressor()
        self.xgboost.load_model('data/models/Xgbtrained.json')
        
        self.prediction = None
        self.predicted = False



    def linear_predict(self):
        return self.linear.predict(self.df_to_predict)


    def xgboost_predict(self):
        return self.xgboost.predict(self.df_to_predict)

    def ranfom_forest_predict(self):
        return "You are in Random forest prediction,but I have't save this model yet. Sorry."



    def model_selection(self):
        match self.model_name:
            case 'Linear':
               self.prediction =  self.linear_predict()
            case 'XGB':
                self.prediction = self.xgboost_predict()
            case 'RandomForest':
                self.prediction = self.ranfom_forest_predict()
        return self.prediction
            

