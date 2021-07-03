from flask import Flask
from cache.cache import cache, config
from flask_restful import Api
from flask_cors import CORS, cross_origin
from api.resources.covidStats import CountryCaseStats, CountryVaccineStats, StateCaseStats, StateVaccineStats, CountyCasesStats\
    , CountyVaccineStats
from api.resources.aerosolve import calc_n_max,calc_co2_series,calc_max_time,\
    calc_n_max_series,get_six_ft_n,get_n_max,merv_to_eff,calc_n_max_ss, aerosolve_data


app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache.init_app(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api.add_resource(CountryCaseStats,'/country_cases_stats')
api.add_resource(CountryVaccineStats,'/country_vaccine_stats')

api.add_resource(StateCaseStats,'/state_cases_stats')
api.add_resource(StateVaccineStats,'/state_vaccine_stats')
api.add_resource(CountyCasesStats,'/county_cases_stats')
api.add_resource(CountyVaccineStats,'/county_vaccine_stats')
api.add_resource(aerosolve_data,'/aerosolve_model')





if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)

