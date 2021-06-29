import pandas as pd
from datetime import date
from datetime import timedelta



today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
yesterday_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
df = pd.read_csv("us-counties.csv")


yesterday_grouped = df[df["date"] == yesterday_date]
yesterday_grouped.to_csv("dataAggegation-" + yesterday_date + ".csv")


today_grouped = df[df["date"] == today_date]
today_grouped.to_csv("dataAggegation-" + today_date + ".csv")

