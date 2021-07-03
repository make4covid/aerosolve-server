#!/bin/sh

curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv --output us-counties.csv
python dataAggegation.py