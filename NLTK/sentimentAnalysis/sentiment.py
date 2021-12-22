from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)
import nltk

nltk.download('vader_lexicon')

page = requests.get('https://www.keepinspiring.me/dr-seuss-quotes/')
soup = BeautifulSoup(page.text, 'html.parser')

quotesTable = soup.find_all(class_='author-quotes')

df = pd.DataFrame({"quotes":quotesTable})

pub = df["quotes"]

quotes = []
for x in pub:
    quotes.append(x.text)
    
newDF = pd.DataFrame({"quotes":quotes})

# print('should be here: ',newDF)

pub = newDF["quotes"]


#Extra \n 
extr = pub.str.find("\n")

pub = pub.replace('\n','',regex=True)
#Quote Dash Doctor
qDDr = pub.str.find(" – Dr. Seuss")
pub = np.where(extr,
                np.where(qDDr,(
                        pub.str.replace(" – Dr. Seuss",'')),
                        pub.str.replace(" \n",'123')),
                np.where(qDDr,(
                        pub.str.replace(" – Dr. Seuss",'')),
                        pub.str))



# newestDF = pd.DataFrame({'quotes':pub})
# pub = newestDF['quotes']
# #end quote
# equot = pub.str.find('”')
# #start quote
# squot = pub.str.find('“')
# pub = np.where(squot,
#                np.where(equot,(
#                          pub.str.replace('”','')),
#                          pub.str.replace('“',''))
#                ,pub.str)


# def test(sentence):
#     analyzer = SentimentIntensityAnalyzer()
#     neuDict = analyzer.polarity_scores(sentence)['neu']
#     posDict = analyzer.polarity_scores(sentence)['pos']
#     negDict = analyzer.polarity_scores(sentence)['neg']
#     compDict = analyzer.polarity_scores(sentence)['compound']
#     print(negDict,neuDict,posDict,compDict)
    
# print(pub[0])


posArray = []
negArray = []
neuArray = []
compArray = []


def sentScores(sentence):
    analyzer = SentimentIntensityAnalyzer()
    neuDict = analyzer.polarity_scores(sentence)['neu']
    posDict = analyzer.polarity_scores(sentence)['pos']
    negDict = analyzer.polarity_scores(sentence)['neg']
    compDict = analyzer.polarity_scores(sentence)['compound']
    posArray.append(posDict)
    negArray.append(negDict)
    neuArray.append(neuDict)
    compArray.append(compDict)
    
    
    
for x in range(len(pub)):
    sentScores(pub[x])

scores = pd.DataFrame({'Neg Array':negArray,
                        'Neu Array':neuArray,
                        'Pos Array':posArray,
                        'Comp Array':compArray,
                        'Quote':pub})

# print('should be here: ',pub[0])

print(scores.head())

print('\n--------------------------------'*2)
print('\n')


avgPosDF = scores["Pos Array"]
avgPosNum = 0
for x in avgPosDF:
    avgPosNum += x
avgPosNum = round(avgPosNum/99,3)
print(avgPosNum,': Avg Pos Num')

avgNegDF = scores["Neg Array"]
avgNegNum = 0
for x in avgNegDF:
    avgNegNum += x
avgNegNum = round(avgNegNum/99,3)
print(avgNegNum,': Avg Neg Num')

avgNeuDF = scores["Neu Array"]
avgNeuNum = 0
for x in avgNeuDF:
    avgNeuNum += x
avgNeuNum = round(avgNeuNum/99,3)
print(avgNeuNum,': Avg Neu Num')

#Just saving my god tier data to a csv file 
# scores.to_csv('datasets/MyDrSeussData.csv')


