import pandas as pd
import numpy as np

pd.options.display.max_columns = None

pd.options.display.max_rows = None

df = pd.read_csv('datasets/spam.csv')

checked = 100    
    
Spam=0
for x in range(checked):
    if df["Category"].loc[x] == "spam":
        Spam+= 1
    else:
        df["Category"].loc[x] = "human"
        
        
print(df.head(checked))

print(str(Spam) + " of " + str(checked) + " are spam")

df = df.set_index('Category')





