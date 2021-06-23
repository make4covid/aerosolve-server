from flask import Flask,jsonify,request
from flask_restful import Resource
from datetime import date
from datetime import timedelta
import requests
import os

class CovidStateStats(Resource):
    def post(self):
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        data = request.get_json()
        # Get Confirmed Covid Case , new case and  Get Deaths Covid Case
        tot_cases = None
        new_case = None
        tot_death = None
        new_death = None
        # Todo parallel send request with python (multi threading)
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
class CovidCountyStats(Resource):
    def post(self):
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        data = request.get_json()
        # Todo Get Confirmed Covid Case for county
        # Todo Get Deaths Covid Case for county
        # Relative Air Humidity
        '''
        Input{
            state: "CO",
            county: "Denver"
        }
        Output{
            humidity: 100
        }
        Docs:
        https://openweathermap.org/current
    
        '''
        relativeHumidity = None
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?q=Denver,CO&appid="+ os.environ.get("openweather_key"))
            relativeHumidity = response.json()["main"][""]["humidity"]
        except:
            pass
        # Get vaccination rate County
        '''
        Input{
         state: "CO",
         county: "Fremont"
        }
        - Vaccination Rate Data for state -> county
        Output{
            "vaccination rate": 
            "series_complete_pop_pct":"22.8"  //Population percentage
            "series_complete_12plus":"10921"  //Number of people
        }
        '''

        vaccineData = None
        try:
            response = requests.get(
                'https://data.cdc.gov/resource/8xkx-amqh.json?date='
                + today_date +
                '&' +
                'recip_state=' + data["state"]
                + '&recip_county='
                + data["county"]
            )  # Google also use this data.
            vaccineData = response.json()
        except:
            pass

        return jsonify(
            vaccinateRatePcr=vaccineData[0]["series_complete_pop_pct"],
            vaccineRateTotal=vaccineData[0]["series_complete_yes"],
            relativeHumidity=relativeHumidity
        )