import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

pd.options.display.max_columns = None

df = pd.read_csv('datasets/petrol_consumption.csv')

X = df.iloc[:, 0:4].values
y = df.iloc[:, 4].values

XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2,random_state=0)
   
sc = StandardScaler()
XTrain = sc.fit_transform(XTrain)
XTest = sc.transform(XTest)
  
regressor = RandomForestRegressor(n_estimators=500,random_state=0)

regressor.fit(XTrain,yTrain)
y_pred = regressor.predict(XTest)

print('Mean Absolute Error:', metrics.mean_absolute_error(yTest, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(yTest, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(yTest, y_pred)))
