from flask import Flask, jsonify, request, make_response, current_app
from flask_restful import Resource
import pandas as pd
from datetime import date, timedelta, datetime
import requests
import numpy as np
import os
from cache.cache import cache
from urllib.parse import urlencode, quote_plus, quote
from pathlib import Path


class CountryCaseStats(Resource):
    # API call
    def post(self):
        data = request.get_json()
        country = data["country"]
        cache_cases_country = cache.get("country " + country + " cases")
        if cache_cases_country is not None:
            data = cache_cases_country.split(" ")

            return make_response(jsonify(
                tot_cases=float(data[0]),
                new_case=float(data[1]),
                tot_death=float(data[2]),
                new_death=float(data[3]),
            ), 200)

        if country == "US":
            url = "https://api.covidtracking.com/v1/us/daily.json"
            r = requests.get(url)
            data_today = r.json()[0]
            data_yesterday = r.json()[1]
            tot_cases = int(data_today["positive"])
            new_case = int(data_today["positive"] - data_yesterday["positive"])
            tot_death = int(data_today["death"])
            new_death = int(data_today["death"] - data_yesterday["death"])
            key = "country " + country + " cases"
            value = str(tot_cases) + " " + str(new_case) + " " + str(tot_death) + " " + str(new_death)
            cache.set(key, value)
            return make_response(jsonify(
                tot_cases=float(tot_cases),
                new_case=float(new_case),
                tot_death=float(tot_death),
                new_death=float(new_death),
            ), 200)
        else:
            return make_response(jsonify(
                reason="Country is not yet configure",
            ), 400)


class CountryVaccineStats(Resource):
    # https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/country_data/United%20States.csv
    # Batch file jobs
    def post(self):
        data = request.get_json()
        country = data["country"]
        cache_vaccine_country = cache.get("country " + country + " vaccine")
        if cache_vaccine_country is not None:
            data = cache_vaccine_country.split(" ")
            total_vaccinations = data[0]
            people_vaccinated = data[1]
            people_fully_vaccinated = data[2]
            people_vaccinated_change = data[3]
            people_fully_vaccinated_change = data[4]
            return make_response(jsonify(
                total_vaccinations=float(total_vaccinations),
                people_vaccinated=float(people_vaccinated),
                people_fully_vaccinated=float(people_fully_vaccinated),
                people_vaccinated_change=float(people_vaccinated_change),
                people_fully_vaccinated_change=float(people_fully_vaccinated_change)
            ), 200)
        if country == "US":
            filename = os.path.join(current_app.root_path, 'data', 'us-vaccine.csv')
            vaccine_data = Path(filename)
            if vaccine_data.is_file():
                df_vaccine = pd.read_csv(filename)
                total_vaccinations = float(df_vaccine.iloc[-1]["total_vaccinations"])
                people_vaccinated = float(df_vaccine.iloc[-1]["people_vaccinated"])
                people_fully_vaccinated = float(df_vaccine.iloc[-1]["people_fully_vaccinated"])
                people_vaccinated_change = float(df_vaccine.iloc[-1]["people_vaccinated"]) - int(
                    df_vaccine.iloc[-2]["people_vaccinated"])
                people_fully_vaccinated_change = float(df_vaccine.iloc[-1]["people_fully_vaccinated"]) - int(
                    df_vaccine.iloc[-1]["people_fully_vaccinated"])
                key = "country " + country + " vaccine"
                value = str(total_vaccinations) + " " + str(people_vaccinated) + " " + str(people_fully_vaccinated) \
                        + " " + str(people_vaccinated_change) + " " + str(people_fully_vaccinated_change)
                cache.set(key, value)

                return make_response(jsonify(
                    total_vaccinations=float(df_vaccine.iloc[-1]["total_vaccinations"]),
                    people_vaccinated=float(df_vaccine.iloc[-1]["people_vaccinated"]),
                    people_fully_vaccinated=float(df_vaccine.iloc[-1]["people_fully_vaccinated"]),
                    people_vaccinated_change=float(df_vaccine.iloc[-1]["people_vaccinated"]) - int(
                        df_vaccine.iloc[-2]["people_vaccinated"])
                    ,
                    people_fully_vaccinated_change=float(df_vaccine.iloc[-1]["people_fully_vaccinated"]) - int(
                        df_vaccine.iloc[-1]["people_fully_vaccinated"])
                ), 200)
            else:
                return make_response(jsonify(
                    reason="No csv file for country vaccine stats",
                ), 400)
        else:
            return make_response(jsonify(
                reason="The requested country is not yet configured",
            ), 400)


class StateCaseStats(Resource):

    def post(self):
        data = request.get_json()
        state = data["state"]
        cache_case_state = cache.get("state " + state + " cases")
        if cache_case_state is not None:
            data = cache_case_state.split(" ")
            return make_response(jsonify(
                tot_cases=float(data[0]),
                new_case=float(data[1]),
                tot_death=float(data[2]),
                new_death=float(data[3]),
            ), 200)

        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        previous_date = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")
        try:
            url = 'https://data.cdc.gov/resource/9mfq-cb36.json?$'
            param = {
                "where": "submission_date between '%s' and '%s'" % (previous_date, today_date),
                'state': state
            }
            url = ("{}{}".format(url, urlencode(param, quote_via=quote)))
            r = requests.get(url)
            data = (sorted(r.json(), key=lambda x: x["submission_date"], reverse=True))[0]
            tot_cases = data["tot_cases"]
            new_case = data["new_case"]
            tot_death = data["tot_death"]
            new_death = data["new_death"]
            key = "state " + state + " cases"
            value = str(tot_cases) + " " + str(new_case) + " " + str(tot_death) + " " + str(new_death)
            cache.set(key, value)
            return make_response(jsonify(
                tot_cases=float(tot_cases),
                new_case=float(new_case),
                tot_death=float(tot_death),
                new_death=float(new_death),
            ), 200)

        except ValueError:
            return make_response(jsonify(
                reason="No data source available",
            ), 400)


class StateVaccineStats(Resource):
    def post(self):
        # Get Vaccination Rate State
        # Aggregate from the API for now
        data = request.get_json()
        state = data["state"]
        cache_vaccine_state = cache.get("state " + state + " vaccine")
        if cache_vaccine_state is not None:
            data = cache_vaccine_state.split(" ")
            return make_response(jsonify(
                total_populate=float(data[0]),
                vaccine_rate_total=float(data[1]),
                vaccinate_rate_pcr=float(data[2])
            ), 200)

        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        previous_date = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")
        try:
            url = 'https://data.cdc.gov/resource/8xkx-amqh.json?$'
            param = {
                "where": "date between '%s' and '%s'" % (previous_date, today_date),
                'recip_state': state
            }
            url = ("{}{}".format(url, urlencode(param, quote_via=quote)))
            r = requests.get(url)
            latest_date = r.json()[0]["date"]
            data = pd.DataFrame(r.json())
            data = data.astype({"series_complete_yes": int, "series_complete_pop_pct": float})
            vaccine_rate_total = int(data.loc[data["date"] == latest_date, "series_complete_yes"].sum())
            data["series_complete_yes*series_complete_pop_pct"] = (100 * (data["series_complete_yes"])) / (
            data["series_complete_pop_pct"]).replace({0: np.inf})
            total_populate = (
                data.loc[data["date"] == latest_date, "series_complete_yes*series_complete_pop_pct"].sum())
            try:
                vaccinate_rate_pcr = (vaccine_rate_total / total_populate) * 100
            except ValueError:
                return make_response(jsonify(
                    reason="Division by 0",
                ), 400)

            key = "state " + state + " vaccine"
            value = str(total_populate) + " " + str(vaccine_rate_total) + " " + str(vaccinate_rate_pcr)
            cache.set(key, value)
            return make_response(jsonify(
                total_populate=float(total_populate),
                vaccine_rate_total=float(vaccine_rate_total),
                vaccinate_rate_pcr=float(vaccinate_rate_pcr)
            ), 200)

        except ValueError:
            return make_response(jsonify(
                reason="Some thing wrong with the data source",
            ), 400)


class CountyCasesStats(Resource):
    def post(self):
        data = request.get_json()
        state = data["state"]
        county = data["county"]
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        cache_data_case = cache.get("county " + state + " " + county + " cases")

        # County Cases Data
        if cache_data_case is not None:
            data = cache_data_case.split(" ")
            total_case = float(data[0])
            total_death = float(data[1])
            new_case = float(data[2])
            new_death = float(data[3])
            return make_response(jsonify(
                totalCase=float(total_case),
                totalDeath=float(total_death),
                newCase=float(new_case),
                newDeath=float(new_death),
            ), 200)
        else:
            try:
                yesterday_grouped = None
                today_grouped = None
                yesterday_filename = os.path.join(current_app.root_path, 'data',
                                                  "dataAggregation-" + yesterday_date + ".csv")
                vaccine_data = Path(yesterday_filename)
                today_filename = os.path.join(current_app.root_path, 'data', "dataAggregation-" + today_date + ".csv")
                yesterday_file = Path(yesterday_filename)
                today_file = Path(today_filename)
                if yesterday_file.is_file() and today_file.is_file():
                    df_yesterday = pd.read_csv(yesterday_filename)
                    df_today = pd.read_csv(today_filename)
                    yesterday_grouped = df_yesterday[df_yesterday["date"] == yesterday_date]
                    today_grouped = df_today[df_today["date"] == today_date]
                # Fall back to the latest file
                else:
                    today_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
                    yesterday_date = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
                    yesterday_filename = os.path.join(current_app.root_path, 'data',
                                                      "dataAggregation-" + yesterday_date + ".csv")
                    today_filename = os.path.join(current_app.root_path, 'data',
                                                  "dataAggregation-" + today_date + ".csv")
                    df_yesterday = pd.read_csv(yesterday_filename)
                    df_today = pd.read_csv(today_filename)
                    yesterday_grouped = df_yesterday[df_yesterday["date"] == yesterday_date]
                    today_grouped = df_today[df_today["date"] == today_date]

                today_ = today_grouped[(today_grouped["state"] == state) & (today_grouped["county"] == county)]
                yesterday_ = yesterday_grouped[(yesterday_grouped["state"] == state) &
                                               (yesterday_grouped["county"] == county)]
                total_case = today_['cases'].values[0]
                total_death = today_['deaths'].values[0]
                new_case = today_['cases'].values[0] - yesterday_['cases'].values[0]
                new_death = today_['deaths'].values[0] - yesterday_['deaths'].values[0]
                key = "county " + state + " " + county + " cases"
                value = str(total_case) + " " + str(total_death) + " " + str(new_case) + " " + str(new_death)
                cache.set(key, value)
                return make_response(jsonify(
                    totalCase=float(total_case),
                    totalDeath=float(total_death),
                    newCase=float(new_case),
                    newDeath=float(new_death),
                ), 200)

            except ValueError:
                return make_response(jsonify(
                    reason="Some thing wrong with the data source",
                ), 400)


class CountyVaccineStats(Resource):
    def post(self):
        data = request.get_json()
        state = data["state"]
        county = data["county"]
        today_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        previous_date = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")
        cache_data_vaccine = cache.get("county " + state + " " + county + " vaccine")
        if cache_data_vaccine is not None:
            data = cache_data_vaccine.split(" ")
            total_populate = float(data[0])
            vaccine_rate_total = float(data[1])
            vaccinate_rate_pcr = float(data[2])
            return make_response(jsonify(
                total_populate=float(total_populate),
                vaccine_rate_total=float(vaccine_rate_total),
                vaccinate_rate_pcr=float(vaccinate_rate_pcr)
            ), 200)
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
                total_populate = int(
                    (float(data["series_complete_yes"]) / float(data["series_complete_pop_pct"])) * 100)
                vaccine_rate_total = data["series_complete_yes"]
                vaccinate_rate_pcr = data["series_complete_pop_pct"]
                key = "county " + state + " " + county + " vaccine"
                value = str(total_populate) + " " + str(vaccine_rate_total) + " " + str(vaccinate_rate_pcr)
                cache.set(key, value)
                return make_response(jsonify(
                    total_populate=float(total_populate),
                    vaccine_rate_total=float(vaccine_rate_total),
                    vaccinate_rate_pcr=float(vaccinate_rate_pcr)
                ), 200)

            except ValueError:
                raise (ValueError)
                return make_response(jsonify(
                    reason="Some thing wrong with the data source",
                ), 400)
