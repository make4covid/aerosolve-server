from flask import Flask,jsonify,request
from flask_restful import Resource
import pandas as pd
from datetime import date, timedelta
import requests
import os
from cache.cache import cache
from urllib.parse import urlencode, quote_plus, quote

# Todo Cache this


class CovidStateCaseStats(Resource):
    def post(self):
        data = request.get_json()
        state = data["state"]
        cache_case_state = cache.get(state + " cases")

        if cache_case_state is not None:
            data = cache_case_state.split(" ")
            return jsonify(
                tot_cases=data[0],
                new_case=data[1],
                tot_death=data[2],
                new_death=data[3],
            )
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        previous_date = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")
        tot_cases = 0
        new_case = 0
        tot_death = 0
        new_death = 0


        try:
            url = 'https://data.cdc.gov/resource/9mfq-cb36.json?$'
            param = {
                "where": "submission_date between '%s' and '%s'" % (previous_date, today_date),
                'state': state
            }
            url = ("{}{}".format(url, urlencode(param, quote_via=quote)))
            r = requests.get(url)

            data = r.json()[0]

            tot_cases = data["tot_cases"]
            new_case = data["new_case"]
            tot_death = data["tot_death"]
            new_death = data["new_death"]
            key = state + " cases"
            value = str(tot_cases) + " " + str(new_case) + " " + str(tot_death) + " " + str(new_death)
            cache.set(key, value)

        except ValueError:
            print(ValueError)
            pass
        return jsonify(
            tot_cases=tot_cases,
            new_case=new_case,
            tot_death=tot_death,
            new_death=new_death,
        )


class CovidStateVaccineStats(Resource):
    def post(self):
        # Get Vaccination Rate State
        # Aggregate from the API for now
        data = request.get_json()
        state = data["state"]
        cache_vaccine_state = cache.get(state + " vaccine")
        if cache_vaccine_state is not None:
            data = cache_vaccine_state.split(" ")
            return jsonify(
                total_populate=(data[0]),
                vaccine_rate_total=(data[1]),
                vaccinate_rate_pcr=(data[2])
            )

        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        previous_date = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")


        vaccinate_rate_pcr = 0
        vaccine_rate_total = 0
        total_populate = 0
        try:
            url = 'https://data.cdc.gov/resource/8xkx-amqh.json?$'
            param = {
                "where": "date between '%s' and '%s'" % (previous_date, today_date),
                'recip_state': state
            }
            url = ("{}{}".format(url, urlencode(param, quote_via=quote)))
            r = requests.get(url)
            data = r.json()
            total_populate = 0
            for item in data:
                vaccine_rate_total += float(item["series_complete_yes"])
                if float(item["series_complete_pop_pct"]) == 0:
                    total_populate += float(item["series_complete_yes"])
                else:
                    total_populate += (100 * float(item["series_complete_yes"])) / float(item["series_complete_pop_pct"])
            try:
                vaccinate_rate_pcr = (vaccine_rate_total / total_populate) * 100
            except:
                pass

            key = state + " vaccine"
            value = str(total_populate) + " " + str(vaccine_rate_total) + " " + str(vaccinate_rate_pcr)
            cache.set(key, value)
        except ValueError:
            print(ValueError)
            pass

        return jsonify(
            total_populate=int(total_populate),
            vaccine_rate_total=int(vaccine_rate_total),
            vaccinate_rate_pcr=int(vaccinate_rate_pcr)
        )

class CovidCountyCasesStats(Resource):
    def post(self):
        data = request.get_json()
        state = data["state"]
        county = data["county"]
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        total_case = 0
        total_death = 0
        new_case = 0
        new_death = 0
        cache_data_case = cache.get(state + " " + county)

        # County Cases Data
        if cache_data_case is not None:
            data = cache_data_case.split(" ")
            total_case = float(data[0])
            total_death = float(data[1])
            new_case = float(data[2])
            new_death = float(data[3])
        else:
            try:
                df_yesterday = pd.read_csv("data/dataAggegation-" + yesterday_date + ".csv")
                df_today = pd.read_csv("data/dataAggegation-" + today_date + ".csv")
                yesterday_grouped = df_yesterday[df_yesterday["date"] == yesterday_date]
                today_grouped = df_today[df_today["date"] == today_date]
                today_ = today_grouped[(today_grouped["state"] == state) & (today_grouped["county"] == county)]
                yesterday_ = yesterday_grouped[(yesterday_grouped["state"] == state) &
                                               (yesterday_grouped["county"] == county)]
                total_case = today_['cases'].values[0]
                total_death = today_['deaths'].values[0]
                new_case = today_['cases'].values[0] - yesterday_['cases'].values[0]
                new_death = today_['deaths'].values[0] - yesterday_['deaths'].values[0]
                key = state + " " + county
                value = str(total_case) + " " + str(total_death) + " " + str(new_case) + " " + str(new_death)
                cache.set(key, value)
            except ValueError:
                print(ValueError)

                pass

        return jsonify(
            totalCase=float(total_case),
            totalDeath=float(total_death),
            newCase=float(new_case),
            newDeath=float(new_death),
        )


class CovidCountyVaccineStats(Resource):
    def post(self):
        data = request.get_json()
        state = data["state"]
        county = data["county"]
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        previous_date = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")

        cache_data_vaccine = cache.get(state + " " + county + " " + "vaccine")
        #County Vaccine Data
        #Get data between 10 days
        total_populate = 0
        vaccine_rate_total = 0
        vaccinate_rate_pcr = 0
        if cache_data_vaccine is not None:
            data = cache_data_vaccine.split(" ")
            total_populate = float(data[0])
            vaccine_rate_total = float(data[1])
            vaccinate_rate_pcr = float(data[2])
        else:
            try:
                url = 'https://data.cdc.gov/resource/8xkx-amqh.json?$'
                param = {
                    "where": "date between '%s' and '%s'" % (previous_date, today_date),
                    'recip_state': state,
                    'recip_county': county + " County"
                }
                url = ("{}{}".format(url, urlencode(param, quote_via=quote)))
                r = requests.get(url)
                data = r.json()[0]
                total_populate = int((float(data["series_complete_yes"]) / float(data["series_complete_pop_pct"])) * 100)
                vaccine_rate_total = data["series_complete_yes"]
                vaccinate_rate_pcr = data["series_complete_pop_pct"]
                key = state + " " + county + " " + "vaccine"
                value = str(total_populate) + " " + str(vaccine_rate_total) + " " + str(vaccinate_rate_pcr)
                cache.set(key, value)
            except ValueError:
                print(ValueError)

                pass

        return jsonify(
            total_populate=float(total_populate),
            vaccine_rate_total=float(vaccine_rate_total),
            vaccinate_rate_pcr=float(vaccinate_rate_pcr)
        )