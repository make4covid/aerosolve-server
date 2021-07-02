from flask import Flask
from cache.cache import cache
from flask_restful import Api
from flask_cors import CORS, cross_origin
from api.resources.covidStats import CovidStateCaseStats,CovidStateVaccineStats, CovidCountyCasesStats\
    , CovidCountyVaccineStats
from api.resources.aerosolve import calc_n_max,calc_co2_series,calc_max_time,\
    calc_n_max_series,get_six_ft_n,get_n_max,merv_to_eff,calc_n_max_ss, aerosolve_data

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60 # 60 seconds
}

app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache.init_app(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'


api.add_resource(CovidStateCaseStats,'/state_cases_stats')

api.add_resource(CovidStateVaccineStats,'/state_vaccine_stats')
api.add_resource(CovidCountyCasesStats,'/county_cases_stats')
api.add_resource(CovidCountyVaccineStats,'/county_vaccine_stats')
api.add_resource(aerosolve_data,'/aerosolve_model')

api.add_resource(calc_n_max,'/indoor/calc_n_max')
api.add_resource(calc_co2_series,'/indoor/calc_co2_series')
api.add_resource(calc_n_max_ss,'/indoor/calc_n_max_ss')
api.add_resource(calc_max_time,'/indoor/calc_max_time')
api.add_resource(calc_n_max_series,'/indoor/calc_n_max_series')
api.add_resource(get_six_ft_n,'/indoor/get_six_ft_n')
api.add_resource(get_n_max,'/indoor/get_n_max')
api.add_resource(merv_to_eff,'/indoor/merv_to_eff')




if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)

