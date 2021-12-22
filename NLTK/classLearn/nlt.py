import requests
import nltk
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download(stopwords)

nintendoWiki = 'https://en.wikipedia.org/wiki/Nintendo'
page = requests.get(nintendoWiki)

soup = BeautifulSoup(page.text, 'html.parser')

text = soup.get_text(separator=' ', strip = True).lower()

#######################################################

#UPDATE TO USE FUZZY WORDNET DOES NOT SUPPORT HOMOPHONES
# homophones = []

# for syn in wordnet.synsets('here'):
#     for lemma in syn.lemmas():
#         if hasattr(lemma, 'homophones'):
#             homophones.append(lemma.homophones()[0].name())

# # print(len(wordnet.synsets('Where')))

# print(homophones)

#######################################################

# syn = wordnet.synsets('boy')
# examp = 1
# print("Name: ",syn[examp].name())
# print("\nDefinition: ", syn[examp].definition())
# print("\nExamples: ", syn[examp].examples())

############################################################

# synonyms = []
# for syn in wordnet.synsets('computer'):
#     for lemma in syn.lemmas():
#         synonyms.append(lemma.name())

# print(synonyms)
# print('\n',wordnet.synsets('computer')[0].definition())

#########################################################

# antonyms = []

# for syn in wordnet.synsets('small'):
#     for lemma in syn.lemmas():
#         if lemma.antonyms():
#             antonyms.append(lemma.antonyms()[0].name())
            
# print(antonyms)
########################################################

# sentences = sent_tokenize(text)

# sentence_words = sentences[6].split()
# first_sentence = ' '.join(sentence_words[-18:])

# nltk_words = word_tokenize(text)

###############################################
 
table = str.maketrans('','',string.punctuation)

words = text.translate(table).split()

cleanedWords = []

myStopWords = stopwords.words()
dropWords = ['nintendo','game']
for x in dropWords:
    myStopWords.append(x)

for token in words:
    if token not in stopwords.words('english') and token not in dropWords:
        cleanedWords.append(token)

freq = nltk.FreqDist(cleanedWords)

freq.plot(20, title = 'Frequency Distributor')
