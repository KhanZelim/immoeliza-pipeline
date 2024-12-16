🔎 **Project Overview**
This web service provides the user with the ability to predict real estate prices in Belgium using one of the available models. The primary objective is to provide accurate price estimates for properties based on their features like location, area, number of rooms, etc.

🤖 **Models**

Prediction is possible using one of the following models:
- XGBoost
- Linear Regression
- Random Forest

**Models stats**


The following metrics were used to evaluate model quality: Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and R².

The best-performing model, XGBoost, achieved an R² score of 0.75 on the test set, indicating that it can explain 75% of the variance in property prices.

The evaluation results of the models are presented in the table below:

<table>
        <tr><th>Model</th><th>MAE</th><th>RMSE</th><th>R2</th></tr>
        <tr><td>LinearRegressor</td><td>66,670.13</td><td>93,728.26</td><td>0.67</td></tr>
        <tr><td>XGBoost</td><td>56,741.12</td><td>82,076.52</td><td>0.75</td></tr>
        <tr><td>Random Forest</td><td>70,506.67</td><td>101,496.22</td><td>0.62</td></tr>
</table>
