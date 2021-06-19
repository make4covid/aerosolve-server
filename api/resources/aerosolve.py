from flask import Flask,jsonify,request
from flask_restful import Resource
import math
from model.aerosolve import Indoors


class aerosolve_data(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        data = request.get_json()
        #calc_max_time safe time given number of occupants | Check the user input, if no user input set default parameter
        #Max safe exposure time given people
        max_time = indoor.calc_max_time(data['nOfPeople'])
        #Max people given exposure time, where is other information?
        max_people = indoor.calc_n_max(data['exp_time'])

        return jsonify({
            "max_hour": max_time # using exp_time_trans
            ,
            "max_people": max_people
        })

class calc_n_max(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        data = request.get_json()
        return jsonify(math.floor(indoor.calc_n_max(data['exp_time'])))
class calc_co2_series(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        data = request.get_json()
        df = indoor.calc_co2_series(data['minimum_time'], data['maximum_time'], data['time_step'], data['risk_mode'])
        return jsonify(df.to_json(orient='records'))

class calc_max_time(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        # Return maximum exposure time
        return jsonify(math.floor(indoor.calc_max_time(data['nOfPeople'])))

class calc_n_max_series(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        data = request.get_json()
        df = indoor.calc_n_max_series(data['minimum_time'], data['maximum_time'], data['time_step'])
        print(df)
        return jsonify(df.to_json(orient='records'))

class get_six_ft_n(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        return jsonify(indoor.get_six_ft_n())
class get_n_max(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        return jsonify(indoor.get_n_max())

class merv_to_eff(Resource):
    def post(self):
        data = request.get_json()
        #Check the user input, if no user input set default parameter
        print(data)
        indoor = Indoors(data)
        return jsonify(indoor.merv_to_eff(data["merv"],data["def_aerosol_radius"]))
class calc_n_max_ss(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors(data)
        # Check the user input, if no user input set default parameter
        data = request.get_json()
        return jsonify(math.floor(indoor.calc_n_max_ss(data['exp_time'])))