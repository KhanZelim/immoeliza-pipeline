import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,root_mean_squared_error
from xgboost import XGBRegressor
import joblib

class Models_trainer:
        def __init__(self) -> None:
                
                self.X_train = pd.read_csv('data/encoded_X_train.csv')
                self.X_test = pd.read_csv('data/encoded_X_test.csv')
                self.y_train = pd.read_csv('data/encoded_y_train.csv')
                self.y_test = pd.read_csv('data/encoded_y_test.csv')
                self.empty_df = None
                self.X_train.drop('Unnamed: 0',axis=1,inplace=True)
                self.X_test.drop('Unnamed: 0',axis=1,inplace=True)
                self.y_test.drop('Unnamed: 0',axis=1,inplace=True)
                self.y_train.drop('Unnamed: 0',axis=1,inplace=True)

        
        
        def train_linearregression(self):
            print('LinearRegression')
            regressor = LinearRegression()
            model = regressor.fit(self.X_train,self.y_train)
            regressor.score(self.X_train,self.y_train)
            self.empty_df = self.X_test[0:0]
            test_prediction = regressor.predict(self.X_test)
            regressor.score(self.X_test,self.y_test)
            print(f'train score : {regressor.score(self.X_train,self.y_train)}')
            print(f'score : {regressor.score(self.X_test,self.y_test)}')
            print(f'MAE : {mean_absolute_error(self.y_test,test_prediction)}')
            print(f'RMSE : {root_mean_squared_error(self.y_test,test_prediction)}')
            return model
        


        def train_xgb(self):
            print('XGBoost')
            regressor = XGBRegressor(n_estimators=1800, subsample=0.8, min_child_weight=3, max_depth=8, learning_rate=0.1, gamma=0.2, colsample_bytree=0.20,reg_alpha=0.1,reg_lambda=1)
            model = regressor.fit(self.X_train, self.y_train, )
            
            regressor.score(self.X_train,self.y_train)
            test_prediction =regressor.predict(self.X_test)
            print(f'train score : {regressor.score(self.X_train,self.y_train)}')
            print(f'score : {regressor.score(self.X_test,self.y_test)}')
            print(f'MAE : {mean_absolute_error(self.y_test,test_prediction)}')
            print(f'RMSE : {root_mean_squared_error(self.y_test,test_prediction)}')
            return model
        
        def saving_LinearRegressionModel(self):
              model = self.train_linearregression()
              joblib.dump(model, '../deployment/data/models/linear_regression_model.joblib')
              joblib.dump(self.empty_df,'empty_df.joblib')

        def saving_XGBmodel(self):
              model = self.train_xgb()
              model.save_model('../deployment/data/models/Xgbtrained.json')
