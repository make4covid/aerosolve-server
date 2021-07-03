#!/bin/sh

curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv --output us-counties.csv
curl https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/United%20States.csv --output data/us-vaccine.csv

python dataAggregation.py