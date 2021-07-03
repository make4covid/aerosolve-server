import pandas as pd
from datetime import date
from datetime import timedelta



today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

yesterday_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
df = pd.read_csv("us-counties.csv")
today_grouped = df[df["date"] == today_date]

if (len(today_grouped) == 0):
    today_grouped = df[df["date"] == (date.today() - timedelta(days=2))]
    today_grouped.to_csv("data/dataAggegation-" + today_date + ".csv")
    yesterday_grouped = df[df["date"] == (date.today() - timedelta(days=3))]
    yesterday_grouped.to_csv("data/dataAggegation-" + yesterday_date + ".csv")
    
else:    
    today_grouped.to_csv("data/dataAggegation-" + today_date + ".csv")
    yesterday_grouped = df[df["date"] == yesterday_date]
    yesterday_grouped.to_csv("data/dataAggegation-" + yesterday_date + ".csv")



