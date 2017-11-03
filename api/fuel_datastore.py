#!/home/anthonyrawlins/anaconda3/bin/python3

import numpy as np
import pyproj as proj

from datetime import datetime, timedelta
from fuel_collector import Collector
from fuel_drivers import Driver

# import rasterio
# import matplotlib.pyplot as plt
# import matplotlib
# from matplotlib import cm


class DataStore:

    def __init__(self):

        self.gda94 = proj.Proj(init='epsg:3112')
        self.data = np.zeros((1, 691, 886), dtype=np.float32)  # Initialise with a single day's values

        self.driver = Driver()
        self.collector = Collector()

        # DEBUG Watching...
        print("This datastore has loaded data for the year:" + self.initial_date.strftime("%Y"))
        print("Starting on: ", self.min_date_held().strftime('%d/%m/%Y'))
        print("Finishing: ", self.max_date_held().strftime('%d/%m/%Y'))

    def set_collector(self, collector):
        """ Allows the DataStore to configure which Collector to use to gather data. """
        self.collector = collector

    def set_driver(self, driver):
        """ Tells the DataStore what storage system driver to use. Defaults to NetCDF4. """
        self.driver = driver

    def load(self, when):
        """ Loads the data for the date supplied, overwriting the internal memory. """
        if self.driver is not None:
            self.data = self.driver.load(when)

        return self.data

    def extend(self, years):
        """ Extends the internal data structure to contain the entire year indicated. """
        for year in years:
            if not self.contains(year):
                self.collector.collect(year)
                if year < self.min_date_held().year:
                    self.data = np.append(self.collector.consume(year), self.data)
                if year > self.min_date_held().year:
                    self.data = np.append(self.data, self.collector.consume(year))

    def contains(self, year):
        """ Returns True if the year supplied is entirely stored in memory. """
        for date in self.date_range_held():
            if date.year == year:
                return True
        return False

    def get_bounds_held(self):
        """ Just the shape of the NDArray. """
        return self.data.shape

    def date_range_held(self):
        """ The entire range of dates as held in memory. """
        return self.data[:, 0, 0]

    def min_date_held(self):
        """ The very first date held in the data structure. """
        return self.data[0, 0, 0][0]

    def max_date_held(self):
        """ The last date held in the data structure. """
        dr = self.min_date_held() + timedelta(days=len(self.data))
        return dr

    def get_3d_array_from_query(self, query):
        """ Uses the spatiotemporal bounds of the query to create a subset from the internal data structure. """
        # extend_if_required
        if not self.query_is_within_bounds(query):
            print("Cannot fulfil request. Sorry.")
            return np.array((0, 0, 0))

        # convert spatial bounds to pixel coords
        s, f = self.index_coords_from_temporal_coords(query.start(), query.finish())
        l, t = self.pixel_coords_from_map_coords(query.left(), query.top())
        r, b = self.pixel_coords_from_map_coords(query.right(), query.bottom())

        print("Debugging:")
        print(">> slicing is...")
        print(s, f, t, l, b, r)

        # y,x are rotated in the datastore so t,l,b,r are not obvious!
        subset = self.data[s:f, t:b+1, l:r+1]
        print(subset.shape)
        subset = subset.reshape(f-s, b+1-t, r+1-l)
        print(subset.shape)
        return subset

    def index_coords_from_temporal_coords(self, start, finish):
        """ Converts the bounding dates to a tuple of array index locations in the internal data structure. """
        print(type(start))
        print(type(finish))

        s = datetime.strptime(start, '%Y%m%d')
        f = datetime.strptime(finish, '%Y%m%d')

        ds = (s - self.min_date_held()).days
        df = (f - self.min_date_held()).days

        print("Delta start: ", ds)
        print("Delta finish: ", df)

        # TODO - Out of temporal range errors!

        return ds, df

    def pixel_coords_from_map_coords(self, lng, lat):
        """ Translates lat/long to pixel coords, by GDA94 (EPSG:3112) projection. """
        x, y = self.gda94(lng, lat)  # meters

        print("X: ", x)
        print("Y: ", y)

        return self.pixel_coords(x, y)  # to pixels

    def pixel_coords(self, x, y):
        """ Computes pixel values from given spatial bounds as determined by GDA94. """
        # Projected bounds on WGS84 (epsg:3857)
        T = -1359735.67040159
        L = -2382330.2876621974
        B = -5045970.303291249
        R = 1632725.0595713349

        xf = 885 / (R - L)
        yf = 690 / (B - T)
        px = (x - L) * xf
        py = (y - T) * yf
        return int(px), int(py)

    def query_is_within_bounds(self, query):
        """ Returns True if the query is entirely within the spatiotemporal area held in memory. """
        validity = False
        fail = False

        print(">>> Bounds of the query:")
        print(">>> t: ", query.top())
        print(">>> l: ", query.left())
        print(">>> b: ", query.bottom())
        print(">>> r: ", query.right())

        if not query.timespan() <= self.get_bounds_held()[0]:
            print("Query out of time bounds.")
            return validity
            # Which direction(s) to expand our DataStore?

        l, t = self.pixel_coords_from_map_coords(query.left(), query.top())
        r, b = self.pixel_coords_from_map_coords(query.right(), query.bottom())

        print(">>> Pixel bounds of the query:")
        print(">>> t: ", t)
        print(">>> l: ", l)
        print(">>> b: ", b)
        print(">>> r: ", r)


        h = b - t
        w = r - l
        if not h <= self.get_bounds_held()[1]:
            print("Query out of bounds. max h: ", self.get_bounds_held()[1])
            fail = True
        if not w <= self.get_bounds_held()[2]:
            print("Query out of bounds. max w: ", self.get_bounds_held()[2])
            fail = True
        if not t >= 0:
            print("Query out of bounds. top is less than 0 ", t)
            fail = True
        if not t <= self.get_bounds_held()[1]:
            print("Query out of bounds. top is greater than ", self.get_bounds_held()[1])
            fail = True
        if not b <= self.get_bounds_held()[1]:
            print("Query out of bounds. bottom is greater than ", self.get_bounds_held()[1])
            fail = True
        if not b >= 0:
            print("Query out of bounds. bottom is less than 0")
            fail = True
        if not l >= 0:
            print("Query out of bounds. left is less than 0")
            fail = True
        if not l <= self.get_bounds_held()[2]:
            print("Query out of bounds. left is greater than", self.get_bounds_held()[2])
            fail = True
        if not r <= self.get_bounds_held()[2]:
            print("Query out of bounds. right is greater than", self.get_bounds_held()[2])
            fail = True
        if not r >= 0:
            print("Query out of bounds. right is less than 0")
            fail = True

        if not fail:
            validity = True
        return validity

