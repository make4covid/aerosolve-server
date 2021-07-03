import unittest
import testcase
from flask import json
import app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.client = self.app.test_client
        self.country = dict({"country": "US"})
        self.state = dict({"state": "CO"})
        self.county = dict({"county": "Denver"})
        self.aerosolve_data = dict({"nOfPeople": 2, "sr_age_factor": 0.68, "sr_strain_factor": 1, "pim": 0.45,
                                    "floor_area": 910, "exp_time": 100, "mean_ceiling_height": 12, "air_exchange_rate": 3,
                                    "recirc_rate": 1,"exhaled_air_inf": 2.04,"def_aerosol_radius": 2,"merv":6,"breathing_flow_rate": 0.29,
                                    "risk_tolerance": 0.1,"mask_eff": 0.90,"mask_fit": 0.95,"max_viral_deact_rate": 0.60,"relative_humidity": 0.6
        })
    def test_country_case_stats(self):

        res = self.client().post('/country_cases_stats', data=json.dumps(self.country), content_type='application/json')
        self.assertEqual(res.status_code, 200)

    # Todo figure out what wrong here

    def test_country_vaccine_stats(self):
        res = self.client().post('/country_vaccine_stats', data=json.dumps(self.country), content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_state_cases_stats(self):
        res = self.client().post('/state_cases_stats', data=json.dumps(self.state),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_state_vaccine_stats(self):
        res = self.client().post('/state_vaccine_stats', data=json.dumps(self.state),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    # Todo figure out what wrong here

    def test_county_cases_stats(self):
        county = dict({
            "state": "Colorado",
            "county": "Denver"
        })
        res = self.client().post('/county_cases_stats', data=json.dumps(county),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)


    def test_aerosolve_model(self):
        res = self.client().post('/aerosolve_model', data=json.dumps(self.aerosolve_data),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
