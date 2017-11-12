#!/home/anthonyrawlins/anaconda3/bin/python3

import pandas as pd
import pyproj as proj
import xarray as xr
from datetime import datetime
from fuel_collector import Collector


class DataStore(Collector):
    data = xr.Dataset()

    def __init__(self):
        super().__init__()
        self.gda94 = proj.Proj(init='epsg:3112')
        # self.data = np.zeros((1, 691, 886), dtype=np.float32)  # Initialise with a single day's values

    def load(self) -> xr.Dataset:
        # TODO - config path properly!
        self.data = xr.open_mfdataset('/home/anthonyrawlins/Data/uom_data/DEAD_FM/DFMC/*_dfmc.nc', concat_dim='Time')
        return self.data

    @staticmethod
    def save(data, where):
        if type(data).is_instance(xr.Dataset):
            data.to_netcdf(where)

    def get_3d_array_from_query(self, query):
        """ Uses the spatiotemporal bounds of the query to create a subset from the internal data structure. """
        # extend_if_required
        # if not self.query_is_within_bounds(query):
        #     print("Cannot fulfil request. Sorry.")
        #     return np.array((0, 0, 0))

        # convert spatial bounds to pixel coords
        s, f = self.index_coords_from_temporal_coords(query.start(), query.finish())
        l, t = self.pixel_coords_from_map_coords(query.left(), query.top())
        r, b = self.pixel_coords_from_map_coords(query.right(), query.bottom())

        print("Debugging:")
        print(">> slicing is...")
        print(s, f, t, l, b, r)

        # y,x are rotated in the datastore so t,l,b,r are not obvious!
        subset = self.data[s:f, t:b + 1, l:r + 1]
        print(subset.shape)
        subset = subset.reshape(f - s, b + 1 - t, r + 1 - l)
        print(subset.shape)
        return subset

    def index_coords_from_temporal_coords(self, start, finish) -> tuple:
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

    def pixel_coords_from_map_coords(self, lng, lat) -> tuple:
        """ Translates lat/long to pixel coords, by GDA94 (EPSG:3112) projection. """
        x, y = self.gda94(lng, lat)  # meters

        print("X: ", x)
        print("Y: ", y)

        return self.pixel_coords(x, y)  # to pixels

    def pixel_coords(self, x, y) -> tuple:
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

    # def query_is_within_bounds(self, query) -> bool:
    #     """ Returns True if the query is entirely within the spatiotemporal area held in memory. """
    #     validity = False
    #     fail = False
    #
    #     print(">>> Bounds of the query:")
    #     print(">>> t: ", query.top())
    #     print(">>> l: ", query.left())
    #     print(">>> b: ", query.bottom())
    #     print(">>> r: ", query.right())
    #
    #     if not query.timespan() <= self.get_bounds_held()[0]:
    #         print("Query out of time bounds.")
    #         return validity
    #         # Which direction(s) to expand our DataStore?
    #
    #     l, t = self.pixel_coords_from_map_coords(query.left(), query.top())
    #     r, b = self.pixel_coords_from_map_coords(query.right(), query.bottom())
    #
    #     print(">>> Pixel bounds of the query:")
    #     print(">>> t: ", t)
    #     print(">>> l: ", l)
    #     print(">>> b: ", b)
    #     print(">>> r: ", r)
    #
    #     h = b - t
    #     w = r - l
    #     if not h <= self.get_bounds_held()[1]:
    #         print("Query out of bounds. max h: ", self.get_bounds_held()[1])
    #         fail = True
    #     if not w <= self.get_bounds_held()[2]:
    #         print("Query out of bounds. max w: ", self.get_bounds_held()[2])
    #         fail = True
    #     if not t >= 0:
    #         print("Query out of bounds. top is less than 0 ", t)
    #         fail = True
    #     if not t <= self.get_bounds_held()[1]:
    #         print("Query out of bounds. top is greater than ", self.get_bounds_held()[1])
    #         fail = True
    #     if not b <= self.get_bounds_held()[1]:
    #         print("Query out of bounds. bottom is greater than ", self.get_bounds_held()[1])
    #         fail = True
    #     if not b >= 0:
    #         print("Query out of bounds. bottom is less than 0")
    #         fail = True
    #     if not l >= 0:
    #         print("Query out of bounds. left is less than 0")
    #         fail = True
    #     if not l <= self.get_bounds_held()[2]:
    #         print("Query out of bounds. left is greater than", self.get_bounds_held()[2])
    #         fail = True
    #     if not r <= self.get_bounds_held()[2]:
    #         print("Query out of bounds. right is greater than", self.get_bounds_held()[2])
    #         fail = True
    #     if not r >= 0:
    #         print("Query out of bounds. right is less than 0")
    #         fail = True
    #
    #     if not fail:
    #         validity = True
    #     return validity
