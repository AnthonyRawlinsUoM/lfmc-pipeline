#!/home/anthonyrawlins/anaconda3/bin/python3

import os
from abc import abstractmethod
import numpy as np
from datetime import datetime, timedelta
from flask_restful import Resource
from flask_jsonpify import jsonify
from fuel_datastore import DataStore


class Model(Resource):
    def __init__(self):
        self.metadata = {}
        self.parameters = {}
        self.outputs = {}
        self.tolerance = 0

    def get(self):
        return jsonify({
            "metadata"  : self.metadata,
            "parameters": self.parameters,
            "outputs"   : self.outputs
        })

    @abstractmethod
    def get_metadata(self):
        return self.metadata

    @abstractmethod
    def get_parameters(self):
        return self.parameters

    @abstractmethod
    def get_outputs(self):
        return self.outputs

    @abstractmethod
    def get_tolerance(self):
        return self.tolerance

    pass


class DeadFuelModel(Model, DataStore):
    def __init__(self):


        # Prefixes
        vapour_prefix = 'VP3pm'
        temp_prefix = 'Tmx'
        precipitation_prefix = 'P'
        dead_fuel_moisture_prefix = 'DFMC'

        path = os.path.abspath('/home/anthonyrawlins/Data/uom_data/DEAD_FM') + '/'

        vapour_url = "http://www.bom.gov.au/web03/ncc/www/awap/vprp/vprph15/daily/grid/0.05/history/nat/"
        max_avg_temp_url = "http://www.bom.gov.au/web03/ncc/www/awap/temperature/maxave/daily/grid/0.05/history/nat/"
        precipitation_url = "http://www.bom.gov.au/web03/ncc/www/awap/rainfall/totals/daily/grid/0.05/history/nat/"
        vapour_path = path + vapour_prefix + "/"
        max_avg_temp_path = path + temp_prefix + "/"
        precipitation_path = path + precipitation_prefix + "/"

        self.tolerance = 0.06  # As a percentage accuracy

        self.metadata = {
            "rainfall"            : "Expressed as percentage gain in water saturation",
            "spatial_resolution"  : "0.05 degrees",
            "data_x_resolution"   : 886,
            "data_y_resolution"   : 691,
            "temporal_granularity": "24 hours",
            "tolerance"           : "+/- 6%"
        }

        self.parameters = {
            "vapour pressure"            : {
                "var"               : "VP3pm",
                "path"              : vapour_path,
                "url"               : vapour_url,
                "prefix"            : vapour_prefix,
                "suffix"            : ".grid",
                "compression_suffix": ".Z"
            },
            "maximum average temperature": {
                "var"               : "T",
                "path"              : max_avg_temp_path,
                "url"               : max_avg_temp_url,
                "prefix"            : temp_prefix,
                "suffix"            : ".grid",
                "compression_suffix": ".Z"
            },
            "precipitation"              : {
                "var"               : "P",
                "path"              : precipitation_path,
                "url"               : precipitation_url,
                "prefix"            : precipitation_prefix,
                "suffix"            : ".grid",
                "compression_suffix": ".Z"
            }
        }

        self.outputs = {
            "fuel moisture": {
                "path"              : path + dead_fuel_moisture_prefix + "/",
                "url"               : "",
                "prefix"            : dead_fuel_moisture_prefix,
                "suffix"            : ".grid",
                "compression_suffix": ".Z"
            }
        }
        print("Loading init data")
        DataStore.__init__(self)

        try:
            self.load()
        except():
            print("Problem loading initial data!")

    def get(self):
        return jsonify({"metadata": self.metadata, "parameters": self.parameters})

    @staticmethod
    def calculate(vp, t, p):
        ea = vp * 0.1
        es = 0.6108 * np.exp(17.27 * t / (t + 237.3))
        d = np.clip(ea - es, None, 0)
        return 6.79 + (27.43 * np.exp(1.05 * d))

    def stringify(self, data):

        print("Creating timeseries for data with shape: ", data.shape)

        series = []
        tol = self.get_tolerance()

        for i in range(0, data.shape[0]):
            print(type(i))

            d = (self.min_date_held() + timedelta(days=i)).strftime("%Y-%m-%dT15:00:00.000Z")

            print(data[i, :, :].shape)
            v = np.mean(data[i, :, :])
            series.append({
                "name"    : d,
                "value"   : v,
                "min"     : v - v * tol,
                "max"     : v + v * tol,
                "rainfall": 0.0,

            })
        r = {
            "name"  : "Nolan",
            # "meta": self.get_metadata(),
            "series": series
        }

        print(r)
        return r

    def get_3d_result_from_query(self, query):

        result = self.get_3d_array_from_query(query)
        if len(result) == 3:
            return {}
        else:
            return self.stringify(result)

    def get_metadata(self):
        return self.metadata

    def get_parameters(self):
        return self.parameters.keys()

    def get_outputs(self):
        return self.outputs.keys()

    def get_tolerance(self):
        return self.tolerance