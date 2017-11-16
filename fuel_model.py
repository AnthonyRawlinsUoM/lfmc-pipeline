#!/home/anthonyrawlins/anaconda3/bin/python3

import os
from abc import abstractmethod
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from flask_restful import Resource
from flask_jsonpify import jsonify
from fuel_datastore import DataStore, Saver
import rasterio
from pathlib2 import Path
import multiprocessing


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


class DeadFuelModel(Model, DataStore, Saver):
    def __init__(self):
        # Prefixes
        vapour_prefix = 'VP3pm'
        temp_prefix = 'Tmx'
        precipitation_prefix = 'P'
        dead_fuel_moisture_prefix = 'DFMC'

        self.path = os.path.abspath('/home/anthonyrawlins/Data/uom_data/DEAD_FM') + '/'

        vapour_url = "http://www.bom.gov.au/web03/ncc/www/awap/vprp/vprph15/daily/grid/0.05/history/nat/"
        max_avg_temp_url = "http://www.bom.gov.au/web03/ncc/www/awap/temperature/maxave/daily/grid/0.05/history/nat/"
        precipitation_url = "http://www.bom.gov.au/web03/ncc/www/awap/rainfall/totals/daily/grid/0.05/history/nat/"
        vapour_path = self.path + vapour_prefix + "/"
        max_avg_temp_path = self.path + temp_prefix + "/"
        precipitation_path = self.path + precipitation_prefix + "/"

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
                "path"              : self.path + dead_fuel_moisture_prefix + "/",
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

    def load(self):
        print("Loading...")
        self.archive_year_range(2015, 2017)  # TODO replace Hardcoded values

    def load_or_make_archive(self, for_year: datetime):
        """ Creates a complete years archive if it doesn\'t exist. """
        print("Compiling dataset.")
        year_data = np.zeros_like(self.data)
        year_file_name = Path(self.path) / self.outputs["fuel moisture"]["prefix"] / ('DFMC_' + for_year.strftime('%Y') + '.nc')
        if not year_file_name.is_file():
            print("Incomplete data for ", for_year.strftime("%Y"))
            # self.fast_collect(self, DataStore.datelist(for_year))  # Collects missing dates' data
            year_data = self.ingest_year(for_year.year)
            DataStore.write_net_cdf4(year_data, year_file_name, for_year)
        return year_data

    @staticmethod
    def calculate(vp, t, p=None):
        ea = vp * 0.1
        es = 0.6108 * np.exp(17.27 * t / (t + 237.3))
        d = np.clip(ea - es, None, 0)
        if p is not None:
            print("Warning: Precipitation is not actually used in this calculation.")
        return 6.79 + (27.43 * np.exp(1.05 * d))

    def ingest_year(self, year: int) -> np.ndarray:
        year_of_data = np.ndarray([365, 691, 886]).astype(np.float32)
        print("Ingesting data for ", str(year))
        for i, date in enumerate(DataStore.datelist(year)):
            try:
                year_of_data[i] = self.ingest(date)
            except():
                print("Cannot gather data for:", date.strftime("%d/%m/%Y"))
                pass
        print("Ingestion for ", str(year), " complete.")
        return year_of_data

    def archive_year_range(self, y1: int, y2: int):
        print("For years:" + str(y1) + " to " + str(y2))
        years_list = DataStore.yearslist(y1, y2)

        for year in years_list:
            self.load_or_make_archive(year)

    def ingest(self, date, save_arc_grid=True) -> np.ndarray:
        model = self
        print("Ingesting dfmc data for:", date.strftime("%d/%m/%Y"))
        o = self.outputs["fuel moisture"]
        dfmc_file_path = o["path"] + o["prefix"] + "_" + date.strftime("%Y%m%d") + o["suffix"]

        if not Path(dfmc_file_path).is_file():
            self.collect(date)

            vapour = DataStore.consume(model, "vapour pressure", date)
            temperature = DataStore.consume(model, "maximum average temperature", date)

            dfmc = self.calculate(vapour, temperature, None)
            # print(dfmc.shape)
            # print(dfmc.dtype)
            # dfmc = dfmc.astype(rasterio.float32, copy=False)
            # print(dfmc.dtype)
            # print(dfmc)

            meta = {'affine': rasterio.Affine(0.05, 0.0, 111.975,
                    0.0, -0.05, -9.974999999999994),
                    'count': 1,
                    'crs': '+proj=latlong',
                    'driver': 'AAIGrid',
                    'dtype': 'float32',
                    'height': 691,
                    'nodata': 99999.8984375,
                    'transform': (111.975, 0.05, 0.0, -9.974999999999994, 0.0, -0.05),
                    'width': 886}
            # Metadata modifications here...

            save_geotiff = False

            if save_geotiff:
                dfmc_file_path += ".tif"
                with rasterio.open(dfmc_file_path, 'w',
                                   driver='GTiff',
                                   **meta) as dest:
                    dest.write(dfmc, 1)
                    dest.close()

            if save_arc_grid:
                # ArcGrid
                with rasterio.open(dfmc_file_path, 'w', **meta) as dest:
                    dest.write(dfmc, 1)
                    dest.close()
        else:
            dfmc = rasterio.open(dfmc_file_path, 'r').read(1)

        return dfmc

    @staticmethod
    def fast_collect(model, dates: list):
        """ Assign a thread per year to speed up collection process. """
        pool = multiprocessing.Pool(processes=8)
        pool.map(model.collect, dates)

    def collect(self, when: datetime):
        """ Collects all input parameters for the model as determined by the metadata. """
        print("Collecting all input parameters data for:", when.strftime("%d/%m/%Y"))
        model = self
        for which in model.get_parameters():
            archive_name = DataStore.archived(model, which, when)
            if not DataStore.archive_exists(model, which, when):
                self.download(model, which, when)
            if DataStore.archive_exists(model, which, when):
                self.expand(archive_name)

    def min_date_held(self) -> datetime:
        return datetime(2015, 1, 1)

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

    def store(self, data, out, when):
        """ Writes the data to an ArcGrid file """

        profile = {}

        # ArcGrid
        with rasterio.open(DataStore.absolute_file_path(self, out, when), 'w', **profile) as dest:
            dest.write(data, 1)
            dest.close()
