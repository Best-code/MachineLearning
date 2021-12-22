import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
 
df = pd.read_csv("Datasets/gamespot_game_reviews.csv")

pd.options.display.max_columns = None
pd.options.display.max_rows = None

reviewsDF = df[["tagline","classifier"]]
print(reviewsDF.head())
taglineList = reviewsDF['tagline'].tolist()
classifierList = reviewsDF['classifier'].tolist()

want = False
dO = input("Would you like to input your own data?\n")
if dO.lower() != 'no':
    inRev = input("Input a review and we will determine if it is negative or positive.\n")
    taglineList.append(inRev)
    inClass = input("Tell us, is this review Positive or Negative\n\'pos\' for positive, \'neg\' for negative\n")
    classifierList.append(inClass)
    want=True
    
countVect = CountVectorizer()
xTrainCounts = countVect.fit_transform(taglineList)

yInput = np.array(classifierList)

tfidf = TfidfTransformer()
xTrainTfidf = tfidf.fit_transform(xTrainCounts) 

XTrain, XTest, yTrain, yTest = train_test_split(xTrainTfidf, 
                                                yInput,
                                                random_state=10,
                                                test_size=.2)

classificationModel = MultinomialNB().fit(XTrain,yTrain)
y_pred = classificationModel.predict(XTest)

numberRight=0
for i in range(len(y_pred)):
    if y_pred[i] == yTest[i]: 
        numberRight = numberRight + 1
        
print("Accuracy for this dataset is: ",numberRight/float(len(y_pred))*100)

if want:
    userNum = len(y_pred)-1
    print("\n---------------------\n")
    print("We predict the rating for your review is: ",y_pred[userNum])
    print("The rating for your review: \""+inRev + "\", was: ", inClass)
    
        

