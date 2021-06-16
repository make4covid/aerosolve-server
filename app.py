from flask import Flask
from flask_restful import Api
from api.resources.covidStats import CovidStateStats, CovidCountyStats
from api.resources.aerosolve import calc_n_max,calc_co2_series,calc_max_time,\
    calc_n_max_series,get_six_ft_n,get_n_max,merv_to_eff,calc_n_max_ss


app = Flask(__name__)
api = Api(app)


api.add_resource(CovidStateStats,'/state_stats')
api.add_resource(CovidCountyStats,'/county_stats')
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
