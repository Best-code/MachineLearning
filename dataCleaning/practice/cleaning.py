import pandas as pd
import numpy as np

pd.options.display.max_columns = None

df = pd.read_csv('datasets/BL-Flickr-Images-Book.csv')

toDrop =  ['Edition Statement',
           'Corporate Author',
           'Corporate Contributors',
           'Former owner',
           'Engraver',
           'Contributors',
           'Issuance type',
           'Shelfmarks']

df.drop(columns=toDrop, inplace=True)

df = df.set_index('Identifier')

regex = r'^(\d{4})'
extr = df['Date of Publication'].str.extract(regex, expand=False)

df['Date of Publication'] = pd.to_numeric(extr)
print(df.head(20))

pub = df['Place of Publication']

london = pub.str.contains('London')

oxford = pub.str.contains('Oxford')

df['Place of Publication'] = np.where(london, 'London',
                                      np.where(oxford, 'Oxford',
                                               pub.str.replace('-',' ')))

university_towns = []
with open('Datasets/university_towns.txt') as file:
    for line in file:
        if '[edit]' in line:
            #store state until anothers found
            state = line
        else:
            university_towns.append((state,line))

towns_df = pd.DataFrame(university_towns,columns=["State","RegionName"])

def getCityState(item):
    if ' (' in item:
        return item[:item.find(' (')]
    elif '[' in item:
        return item[:item.find('[')]
    else:
        return item
    
towns_df = towns_df.applymap(getCityState)

olympics_df = pd.read_csv('datasets/olympics.csv', header=1)

new_names = {'Unnamed: 0': 'Country',
             '? Summer': 'Summer Olympics',
             '01 !': 'Gold',
             '02 !': 'Silver',
             '03 !': 'Bronze',
             '? Winter': 'Winter Olympics',
             '01 !.1': 'Gold.1',
             '02 !.1': 'Silver.1',
             '03 !.1': 'Bronze.1',
             '? Games': '# Games',
             '01 !.2': 'Gold.2',
             '02 !.2': 'Silver.2',
             '03 !.2': 'Bronze.2'}

olympics_df.rename(columns=new_names, inplace=True)

# print(olympics_df.head())