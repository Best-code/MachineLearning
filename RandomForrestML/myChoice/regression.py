import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import random

df = pd.read_csv('datasets/tv_shows.csv')

print(df.head())
pd.options.display.max_columns = None
pd.options.display.max_rows= None

toDrop = ["Rotten Tomatoes",
          "Unnamed: 0",
          "type"
          ]
#removes unnecessary columns
df.drop(columns=toDrop, inplace = True)    
#Changes identifier to title
# df = df.set_index("Title")

#Finds non digits
regex = r'(\D)'
    
pub = df['Age'] 
#Changes regex/non digits and 'all' to 0
extr = np.where(pub.str.contains('all'),pub.str.replace('all','0'),pub.str.replace(regex,""))
#changing all strings above ^^^ to numbers
df['Age'] = pd.to_numeric(extr)

# df.fillna(0,inplace=True)
df.dropna(inplace=True)
    
ageTarget = {"Age":"Target Age >"}
df.rename(columns=ageTarget, inplace=True)


# cond1=df["IMDb"]<6
# cond2=df["IMDb"]>7
# df = df[cond1 | cond2]
# print(len(df)/3137)
# print(df.head())

# Saves the new beautiful clean file to that location
# df.to_csv('datasets/tvshowsCleansed.csv')

#MACHINE LEARNING

X = df.iloc[:, [1,2,4,5,6,7]].values
y = df.iloc[:, 3].values

dtet = X
custom = input("Would you like to do a custom check?\n")
printCustom = False
if custom.lower() != 'no':
    iX = []    
    words = ['Year','Target Age >', 'Netflix',' Hulu',' Prime Video',' Disney+']
    for x in range(len(words)):
        iX.append(input(words[x]+'\n'))
    iX = [float(x) for x in iX]
    iX = np.array(iX)
    X = np.concatenate((X,[iX]))
    y = np.concatenate((y, [0]))
    printCustom = True


XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2,random_state=0)

sc = StandardScaler()
XTrain = sc.fit_transform(XTrain)
XTest = sc.transform(XTest)

  
regressor = RandomForestRegressor(n_estimators=256)

regressor.fit(XTrain,yTrain)
y_pred = regressor.predict(XTest)

print('\n'*5)

print('\n--------------------\n')
print('Mean Absolute Error:', metrics.mean_absolute_error(yTest, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(yTest, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(yTest, y_pred)))

if printCustom:
    print('\n--------------------\n')
    print('\nMy prediction for your inputs is a ',round(y_pred[len(y_pred)-1],2),' / 10 score!\n')

print("\n--------------------\n")

numToPredict = random.randint(0,len(y_pred)-1)
accuracy = y_pred[numToPredict]/y[numToPredict]
if accuracy > 1:
    accuracy %= 1
    accuracy -= 1
    accuracy *= -1
    
print('Title: ',df["Title"].iloc[numToPredict],'\nYear', X[numToPredict,0],'\nTarget Age ',X[numToPredict,1],'\nActual Answer: ',y[numToPredict],
      '\nPredicted Answer: ', y_pred[numToPredict],'\nAccuracy: ',accuracy)








