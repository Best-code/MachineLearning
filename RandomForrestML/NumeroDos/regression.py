import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
# import random

df = pd.read_csv('datasets/train.csv')

pd.options.display.max_columns = None
pd.options.display.max_rows = None
# df.set_index('id')
#Maybe run a sentiment analysis on the description

toDrop = ['id','description','neighbourhood',
          'host_since','host_has_profile_pic',
          'first_review','thumbnail_url',
          'host_identity_verified','longitude',
          'instant_bookable','last_review','name',
          'latitude','accommodates','number_of_reviews'
          ]

newDF = df.drop(columns=toDrop)
newDF.dropna(inplace = True) 

didUser = False
scndFor = True
userInput = input('Would you like to input your own data?\n')
if 'no' not in userInput.lower():
    if userInput == 'auto':
        scndFor = False
    inputs = []
    words = []
    columns = []
    for i in newDF.columns:
        columns.append(i)
    test = ['apartment','Entire home/apt',6,'1','real bed','flexible',True,'NYC','100%','100',10019,0,1]
    for x in newDF.columns[1:]:
        words.append(x)
    if scndFor:
        for x in range(len(words)):
            if x not in [2,6,10,11,12]:
                inputs.append(input(words[x]+'\n'))
            elif x  in [2,10,11,12]:
                inputs.append(int(input(words[x]+'\n')))
                print(inputs[2]+10)
            else:
                inputs.append(bool(input(words[x]+'\n')))
                print(inputs[2]+10)
        for x in range(len(inputs)-1):
            newDF = newDF.append({columns[x+1]:words[x]},ignore_index=True)
    else:
        for x in range(len(inputs)-1):
            newDF = newDF.append({columns[x+1]:words[x]},ignore_index=True)
        
    newDF = newDF.append({columns[0]:5},ignore_index=True)
    didUser = True
else:
    print("You selected not to input data")

#Host response rate
hrp = newDF['host_response_rate']
newDF['host_response_rate'] = pd.to_numeric(np.where(hrp.str.contains('%'),
                                       hrp.str.replace('%',''),
                                       hrp.str))

newDF['host_response_rate'] = newDF['host_response_rate'].div(100)
newDF['review_scores_rating'] = newDF['review_scores_rating'].div(100)


#cleaning_fee
cf = newDF['cleaning_fee']
newDF['cleaning_fee'] = pd.to_numeric(np.where(cf == (True),
                                       cf.replace(True,'1'),
                                       cf.replace(False,'0')))

bedTypes = df['bed_type'].unique()
cancelTypes = df['cancellation_policy'].unique()
propTypes = df['property_type'].unique()
roomTypes = df['room_type']
citys = df['city']


# #First 5 digits
regex = r'^(\d{5})'
newDF = newDF[newDF['zipcode'].str.len() == 5]
newDF['zipcode'] = pd.to_numeric(newDF['zipcode'])

wordsDf = newDF

def ez(listOfStrings):
    myDict = {}
    counter=0
    for word in listOfStrings:
        if(word not in myDict.keys()):
            myDict[word]=counter
            counter+=1
    return myDict

bedRun = ez(bedTypes)
canRun = ez(cancelTypes)
propRun = ez(propTypes)
roomRun = ez(roomTypes)
citysRun = ez(citys)

newDF = newDF.applymap(lambda bed: bed if bed not in bedRun.keys() else bedRun[bed])
newDF = newDF.applymap(lambda can: can if can not in canRun.keys() else canRun[can])
newDF = newDF.applymap(lambda prop: prop if prop not in propRun.keys() else propRun[prop])
newDF = newDF.applymap(lambda room: room if room not in roomRun.keys() else roomRun[room])
newDF = newDF.applymap(lambda citys: citys if citys not in citysRun.keys() else citysRun[citys])



# newDF.to_csv('datasets/newData.csv')

# print(newDF['amenities'].iloc[123].split(','))
# print(len(newDF['amenities'].iloc[123].split(',')))


amenityCount = []
for x in range(len(newDF['amenities'])):
    if x < len(newDF['amenities']):
        amenityCount.append(len(newDF['amenities'].iloc[x].split(',')))
    # else:
    #     amenityCount.append(len(newDF['amenities'].iloc[x]))
newDF['amenityCount'] = amenityCount
    
# =============================================================================
# MACHINE LEARNING STARTS HERE
# =============================================================================

# X = newDF.iloc[:, [2,3,5,6,7,8,9,10,11,12,13,14]].values
X = newDF.iloc[:, [1,2,4,5,6,7,8,9,10,11,12,13]].values

y = newDF.iloc[:, 0].values

XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2,random_state=0)

sc = StandardScaler()
XTrain = sc.fit_transform(XTrain)
XTest = sc.transform(XTest)

  
regressor = RandomForestRegressor(n_estimators=256, random_state=0)

regressor.fit(XTrain,yTrain)
y_pred = regressor.predict(XTest)



    
print('\n--------------------\n')
print('Mean Absolute Error:', metrics.mean_absolute_error(yTest, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(yTest, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(yTest, y_pred)))

numToPred = 8375
post = round(y_pred[numToPred]*10,2)
print('I predict the log price is going to be: ', '$',str(post))

if didUser:
    #The very last num  in the array if a user has inputted
    numToPred = 8376
    post = round(y_pred[numToPred]*10,2)
    print('I predict the log price is going to be: ', '$',str(post))



