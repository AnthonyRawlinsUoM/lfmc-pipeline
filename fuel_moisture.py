#!/home/anthonyrawlins/anaconda3/bin/python3

# OS & Web
import argparse
import os

# Server
from flask import Flask
from flask_restful import Api

# Fuel API
from fuel_api import ApiHelp, SpatiotemporalRequestHandler

THREADS = 8
PORT = 5000
PROJECT_ROOT = os.getcwd()
app = Flask(__name__)
api = Api(app)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-p", "--port", help="Port for the server to run on")
    parser.add_argument("-t", "--threads",
                        help="Number of worker threads for the server (Max: half your physical cores!)")
    parser.add_argument("-d", "--data", help="Root path of the datastore")
    args = parser.parse_args()

    if args.verbose:
        print("verbosity turned on")

    global PROJECT_ROOT
    global PORT
    global THREADS

    PORT = args.port
    THREADS = args.threads
    PROJECT_ROOT = args.data

    api.add_resource(SpatiotemporalRequestHandler,
                     '/api/fuel/models/<models>/<lng1>/<lat1>/<lng2>/<lat2>/time/<start>/<finish>')
    api.add_resource(ApiHelp, '/')


if __name__ == '__main__':
    main()
    app.run(port=PORT)
