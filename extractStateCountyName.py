import pandas as pd



df = pd.read_csv("us-counties.csv")

'''
data = dict()
for index, row in df.iterrows():
    county = []
    if row['state'] in data:
        county = data[row['state']]
    if row['county'] in county:
        continue
    county.append(row['county'])
    data[row['state']] = county
'''

state =  df['state'].unique()
print(state)