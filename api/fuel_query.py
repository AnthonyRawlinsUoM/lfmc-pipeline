#!/home/anthonyrawlins/anaconda3/bin/python3

from flask_restful import Resource
from flask_jsonpify import jsonify


class SpatiotemporalQuery(Resource):
    def __init__(self, t1, t2, lng1, lat1, lng2, lat2):
        self.temporal = {
                'start': t1
        }
        if t2 is not None:
            self.temporal['finish'] = t2
        else:
            self.temporal['finish'] = t1  # ie., the same as start date

        self.spatial = {
                'left': lng1,
                'bottom': lat2,
                'top': lat1,
                'right': lng2
        }

    def get(self):
        return jsonify({"Bounds": [self.temporal, self.spatial]})

    def upper(self):
        return (self.temporal['finish'], self.spatial['top'], self.spatial['right'])

    def lower(self):
        return (self.temporal['start'], self.spatial['bottom'], self.spatial['left'])

    def start(self):
        return self.temporal['start'].strftime('%Y%m%d')

    def finish(self):
        return self.temporal['finish'].strftime('%Y%m%d')

    def top(self):
        return self.spatial['top']

    def bottom(self):
        return self.spatial['bottom']

    def left(self):
        return self.spatial['left']

    def right(self):
        return self.spatial['right']

    def timespan(self):
        return (self.temporal['finish'] - self.temporal['start']).days
