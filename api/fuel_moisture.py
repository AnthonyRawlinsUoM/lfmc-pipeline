#!/home/anthonyrawlins/anaconda3/bin/python3

# OS & Web
import argparse


# Server
from flask import Flask, request
from flask_restful import Resource, Api

# Fuel API

from fuel_api import ApiHelp, SpatioTemporalRequestHandler
from fuel_collector import FileNameWrangler

app = Flask(__name__)
api = Api(app)

# api.add_resource(Models, '/api/models')

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

    PORT = args.port
    THREADS = args.threads
    PROJECT_ROOT = args.data
    #FileNameWrangler().ensure_dir(PROJECT_ROOT)  #or die("Data dir doesn't exist or not writable!")

    api.add_resource(SpatioTemporalRequestHandler,
                     '/api/fuel/models/<models>/<lng1>/<lat1>/<lng2>/<lat2>/time/<start>/<finish>')
    api.add_resource(ApiHelp, '/')


if __name__ == '__main__':
    main()
    app.run(port=PORT)
