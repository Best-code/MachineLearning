import pandas as pd
import numpy as np

df = pd.read_csv("datasets/tv_shows.csv")

pd.options.display.max_columns = None
pd.options.display.max_rows=None

toDrop = ["Rotten Tomatoes",
          "Unnamed: 0",
          "type"
          ]

df.drop(columns=toDrop, inplace = True)    

df = df.set_index("Title")


regex = r'(\D)'
    
pub = df['Age'] 
extr = np.where(pub.str.contains('all'),pub.str.replace('all','0'),pub.str.replace(regex,""))
    
df['Age'] = pd.to_numeric(extr)
    
ageTarget = {"Age":"Target Age >"}
df.rename(columns=ageTarget, inplace=True)

print(df.iloc[5610])