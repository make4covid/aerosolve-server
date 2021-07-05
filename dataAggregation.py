import pandas as pd
from datetime import date
from datetime import timedelta

import time

start = time.time()

today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

yesterday_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
df = pd.read_csv("http://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
# df = pd.read_csv("us-counties.csv")
today_grouped = df[df["date"] == today_date]

if (len(today_grouped) == 0):
    new_today_date = ((date.today() - timedelta(days=2))).strftime("%Y-%m-%d")
    today_grouped = df[df["date"] == new_today_date]
    today_grouped.to_csv("data/dataAggregation-" + new_today_date + ".csv")
    new_yesterday_date = ((date.today() - timedelta(days=3))).strftime("%Y-%m-%d")
    yesterday_grouped = df[df["date"] == new_yesterday_date]
    yesterday_grouped.to_csv("data/dataAggregation-" + new_yesterday_date + ".csv")
    
else:    
    today_grouped.to_csv("data/dataAggregation-" + today_date + ".csv")
    yesterday_grouped = df[df["date"] == yesterday_date]
    yesterday_grouped.to_csv("data/dataAggregation-" + yesterday_date + ".csv")

end = time.time()
print(end - start)

# Todo clean csv file. Only keep 4 consecutive days


