#!/home/anthonyrawlins/anaconda3/bin/python3

from datetime import datetime
from flask_restful import Resource
from flask_jsonpify import jsonify
from json_tricks import dumps

from fuel_model import DeadFuelModel
from fuel_query import SpatiotemporalQuery

class ApiHelp(Resource):
    def get(self):
        return {"See API": "Help goes here."}  # TODO!


class SpatioTemporalRequestHandler(Resource):
    """ Responds to well-formed JSON requests with JSON formatted subsets of our data. """

    def __init__(self):

        self.models_impl = {}
        self.models_impl["nolan"] = DeadFuelModel()
        self.start = datetime.now()
        self.finish = datetime.now()
        self.lat1 = 0.
        self.lng1 = 0.
        self.lat2 = 0.
        self.lng2 = 0.

    def get(self, models, start, finish, lng1, lat1, lng2=None, lat2=None):
        result = []
        self.start = datetime.strptime(start, "%Y%m%d")
        self.finish = datetime.strptime(finish, "%Y%m%d")
        self.lat1 = float(lat1)
        self.lng1 = float(lng1)
        self.lat2 = float(lat2) or 0
        self.lng2 = float(lng2) or 0

        modelchoices = models.split(',')

        q = SpatiotemporalQuery(self.start, self.finish, self.lng1, self.lat1, self.lng2, self.lat2)

        for i, m in enumerate(modelchoices):
            for k, v in self.models_impl.items():
                if k == m:
                    result.append(v.get_3d_array_from_query(q))

        print(dumps(result))
        return dumps(result)
    pass
