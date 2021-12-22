import pandas as pd
import numpy as np
from sklearn import svm, metrics
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)
import tensorflow as tf
import time

import turtle
from turtle import Screen, Turtle

dO = False
drawOwn = input("Would you like to draw your own number\n")
if drawOwn.lower() != 'no':
    screen = Screen()
    turtle.setup(250,250)
    screen.screensize(500,500)
    t = Turtle("turtle")
    t.speed(-1)
    
    
    def dragging(x, y):  # These parameters will be the mouse position
        t.ondrag(None)
        t.setheading(t.towards(x, y))
        t.goto(x, y)
        t.ondrag(dragging)
    
    def clickRight(x,y):
        t.clear()
    
    def main():  # This will run the program
        turtle.listen()
        
        t.ondrag(dragging)  # When we drag the turtle object call dragging
        turtle.onscreenclick(clickRight, 3)
    
        screen.mainloop()  # This will continue running main() 
    
    main()
    d0 = True
    if input():
        ts = turtle.getscreen()
        ts.getcanvas().postscript(file='myNum.png')
    

        



(XTrain,yTrain),(XTest,yTest) = tf.keras.datasets.mnist.load_data()

XTrain = XTrain.reshape(60000,784)
XTest = XTest.reshape(10000,784)

XTrain = XTrain[:64, :]
yTrain = yTrain[:64]
XTest = XTest[:100, :]
yTest = yTest[:100]

model = svm.SVC()
model.fit(XTrain,yTrain)

y_pred = model.predict(XTest)


index_to_compare = 99
#for x in range(0,index_to_compare):
 #   title = ('True: ' + str(yTest[x]) + ', Prediction: ' + str(y_pred[x]))
  #  plt.imshow(XTest[x].reshape(28,28),cmap='gray',)
   # plt.title(title)
   # plt.grid(None)
   # plt.axis('off')
   # plt.show()
    #time.sleep(1)

acc = metrics.accuracy_score(yTest,y_pred)
print('\nAccuracy: ',acc)

digits = pd.DataFrame.from_dict(yTrain)

ax = sns.countplot(x=0,data=digits)

ax.set_title("Distribution od Digit Images in Test Set")
ax.set(xlabel='Digit')
ax.set(ylabel='Count')
plt.show()

cm = metrics.confusion_matrix(yTest,y_pred)
# print(cm)

ax = plt.subplots(figsize=(9,6))

sns.heatmap(cm,annot=True)

ax[1].title.set_text("SVC Prediction Accuracy")
ax[1].set_xlabel("Predicted Digit")
ax[1].set_ylabel("True Digit")

plt.show()


