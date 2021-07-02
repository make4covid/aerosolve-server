from flask import Flask,jsonify,request
from flask_restful import Resource
import pandas as pd
from datetime import date
from datetime import timedelta
import requests
import os
from cache.cache import cache


class CovidStateStats(Resource):
    def post(self):
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        data = request.get_json()
        # Get Confirmed Covid Case , new case and  Get Deaths Covid Case
        tot_cases = None
        new_case = None
        tot_death = None
        new_death = None

        try:
            response = requests.get(
                'https://data.cdc.gov/resource/9mfq-cb36.json?submission_date=' + "2021-06-20" + '&state=' + data[
                    "state"])
            response_json = response.json()
            tot_cases = response_json[0]["tot_cases"]
            new_case = response_json[0]["new_case"]
            tot_death = response_json[0]["tot_death"]
            new_death = response_json[0]["new_death"]
        except ValueError:
            print(ValueError)
            pass

        # Get Vaccination Rate State
        # Aggregate from the API for now
        vaccineData = None
        vaccinateRatePcr = 0
        vaccineRateTotal = 0
        totalPopulate = 0
        try:
            response = requests.get(
                'https://data.cdc.gov/resource/8xkx-amqh.json?date='
                + today_date +
                '&' +
                'recip_state=' + data["state"]
            )  # Google also use this data.
            vaccineData = response.json()
            for item in vaccineData:
                vaccineRateTotal += float(item["series_complete_yes"])
                if float(item["series_complete_pop_pct"]) == 0:
                    totalPopulate += float(item["series_complete_yes"])
                else:
                    totalPopulate += (100 * float(item["series_complete_yes"])) / float(item["series_complete_pop_pct"])
            vaccinateRatePcr = (vaccineRateTotal / totalPopulate) * 100
        except ValueError:
            print(ValueError)
            pass

        # Or read from file

        # Get Relative Air Humidity
        relativeHumidity = None

        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?q=Denver,CO&appid=" + os.environ.get(
                    "openweather_key"))
            relativeHumidity = response.json()["main"][""]["humidity"]
        except:
            pass



        return jsonify(
            tot_cases=tot_cases,
            new_case=new_case,
            tot_death=tot_death,
            new_death=new_death,
            vaccinateRatePcr=vaccinateRatePcr,
            vaccineRateTotal=vaccineRateTotal,
            relativeHumidity=relativeHumidity
        )


# Todo How to cache this?
class CovidCountyStats(Resource):


    def post(self):
        data = request.get_json()
        state = data["state"]
        county = data["county"]

        cache_data = cache.get(state + " " + county)

        if cache_data is not None:
            data = cache_data.split(" ")
            print(data)
            return jsonify(
                totalCase=float(data[0]),
                totalDeath=float(data[1]),
                newCase=float(data[2]),
                newDeath=float(data[3])
            )

        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")

        try:
            df_yesterday = pd.read_csv("dataAggegation-" + yesterday_date + ".csv")
            df_today = pd.read_csv("dataAggegation-" + today_date + ".csv")
            yesterday_grouped = df_yesterday[df_yesterday["date"] == yesterday_date]
            today_grouped = df_today[df_today["date"] == today_date]
            today_ = today_grouped[(today_grouped["state"] == state) & (today_grouped["county"] == county)]
            yesterday_ = yesterday_grouped[(yesterday_grouped["state"] == state) & (yesterday_grouped["county"] == county)]
        except:
            pass

        total_case = 0
        total_death = 0
        new_case = 0
        new_death = 0
        try:
            total_case = today_['cases'].values[0]
            total_death = today_['deaths'].values[0]
            new_case = today_['cases'].values[0] - yesterday_['cases'].values[0]
            new_death = today_['deaths'].values[0] - yesterday_['deaths'].values[0]
            key = state + " " + county
            value = str(total_case) + " " + str(total_death) + " " + str(new_case) + " " + str(new_death)
            print("Value:",value)
            cache.set(key, value)
            print("Set Cache:",cache)
        except:
            print("Fail cache")
            pass




        return jsonify(
            totalCase=float(total_case),
            totalDeath=float(total_death),
            newCase=float(new_case),
            newDeath=float(new_death)
        )