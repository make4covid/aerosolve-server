from flask import Flask,jsonify,request
from flask_restful import Resource
import math
from model.Indoor import Indoors


def set_parameter(object,data):
    # Physical Parameters
    physical_params = object.physical_params

    if "floor_area" in data:
        physical_params[0] = data["floor_area"]
    if "mean_ceiling_height" in data:
        physical_params[1] = data["mean_ceiling_height"]
    if "air_exchange_rate" and "recirc_rate" in data:
        air_exchange_rate = data["air_exchange_rate"]
        outdoor_air_fraction = air_exchange_rate / (air_exchange_rate + data["recirc_rate"])
        physical_params[3] = outdoor_air_fraction
    if "def_aerosol_radius" and "merv" in data:
        aerosol_filtration_eff = Indoors.merv_to_eff(data["merv"], data["def_aerosol_radius"])
        physical_params[4] = aerosol_filtration_eff
    if "relative_humidity" in data:
        physical_params[5] = data["relative_humidity"]
    object.physical_params = physical_params

    # Physiological Parameters
    physio_params = object.physio_params
    if "breathing_flow_rate" in data:
        physio_params[0] = data["breathing_flow_rate"] * 60 / 35.3147

    if "def_aerosol_radius" in data:
        physio_params[1] = data["def_aerosol_radius"]

    object.physio_params = physio_params

    disease_params = object.disease_params
    # Disease Parameters
    if "exhaled_air_inf" in data:
        disease_params[0] = data["exhaled_air_inf"] * 35.3147
    if "max_viral_deact_rate" in data:
        disease_params[1] = data["max_viral_deact_rate"]

    object.disease_params = disease_params

    # Precautionary Parameters
    mask_passage_prob = 0.1
    risk_tolerance = 0.1
    if "sr_strain_factor" in data:
        object.sr_strain_factor = data["sr_strain_factor"]
    if "sr_age_factor" in data:
        object.sr_age_factor = data["sr_age_factor"]

    if "mask_eff" and "mask_fit" in data:
        mask_real_eff = data["mask_eff"] * data["mask_fit"]
        mask_passage_prob = round(1 - mask_real_eff, 4)  # 1 = no masks, ~0.1 cloth, <0.05 N95

    if "risk_tolerance" in data:
        risk_tolerance = data["risk_tolerance"]

    prec_params = [mask_passage_prob, risk_tolerance]
    pi = 0
    if "risk_mode" in data:
        if data["risk_mode"] == 'conditional':
            prevalence = 0
            pi = prevalence / 100000
    if "pim" in data:
        pim_input = data["pim"]
        object.percentage_sus = 1 - (pi + pim_input)
    object.prec_params = prec_params
    object.calc_vars()
    return object


class aerosolve_data(Resource):
    def post(self):
        indoor = Indoors()
        data = request.get_json()
        indoor = set_parameter(indoor, data)
        max_time = indoor.calc_max_time(data["nOfPeople"])
        max_people = indoor.calc_n_max(data["exp_time"])

        return jsonify({
            "max_hour": max_time # using exp_time_trans
            ,
            "max_people": max_people
        })


class calc_n_max(Resource):
    def post(self):
        indoor = Indoors()
        data = request.get_json()
        indoor = set_parameter(indoor, data)
        return jsonify(math.floor(indoor.calc_n_max(data['exp_time'])))


class calc_co2_series(Resource):
    def post(self):
        indoor = Indoors()
        data = request.get_json()
        set_parameter(indoor, data)
        df = indoor.calc_co2_series(data['minimum_time'], data['maximum_time'], data['time_step'], data['risk_mode'])
        return jsonify(df.to_json(orient='records'))


class calc_max_time(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors()
        set_parameter(indoor, data)
        risk_type = "conditional"
        if "risk_type" in data:
            risk_type = data["risk_type"]
        return jsonify(math.floor(indoor.calc_max_time(data['nOfPeople'], risk_type)))

class calc_n_max_series(Resource):
    def post(self):
        indoor = Indoors()
        data = request.get_json()
        set_parameter(indoor, data)
        df = indoor.calc_n_max_series(data['minimum_time'], data['maximum_time'], data['time_step'])
        print(df)
        return jsonify(df.to_json(orient='records'))

class get_six_ft_n(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors()
        set_parameter(indoor, data)
        return jsonify(indoor.get_six_ft_n())
class get_n_max(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors()
        set_parameter(indoor, data)
        return jsonify(indoor.get_n_max())

class merv_to_eff(Resource):
    def post(self):
        data = request.get_json()
        indoor = Indoors()
        set_parameter(indoor, data)
        return jsonify(indoor.merv_to_eff(data["merv"],data["def_aerosol_radius"]))
class calc_n_max_ss(Resource):
    def post(self):
        indoor = Indoors()
        data = request.get_json()
        set_parameter(indoor, data)
        return jsonify(math.floor(indoor.calc_n_max_ss(data['exp_time'])))