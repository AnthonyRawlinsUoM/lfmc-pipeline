#!/home/anthonyrawlins/anaconda3/bin/python3

import urllib.request
from urllib.error import URLError
import subprocess
import rasterio
import multiprocessing
from fuel_utils import FileNameWrangler, TimeWrangler


class Collector(FileNameWrangler, TimeWrangler):

    def fast_collect(self, years):
        """ Assign a thread per year to speed up collection process. """
        pool = multiprocessing.Pool(processes=8)
        pool.map(self.collect, years)

    def download(self, which, when):
        """Downloads and extracts data from BOM based on date range"""
        what = FileNameWrangler.url(self, which, when)
        where = FileNameWrangler.absolute_filepath(self, which, when)

        try:
            urllib.request.urlretrieve(what, where)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            # else:
            # everything is fine
        print('Download complete')
        return where

    def expand(self, what, where):
        """ OS level decompression algorithm; spawns a subprocess. """
        print("Expanding: " + what + " to " + where)
        subprocess.run(["uncompress", "-k", where + what, "/dev/null"], stdout=subprocess.PIPE)

    def collect(self, year):
        """ Collects all input parameters for the model as determined by the metadata. """
        for which in self.params:
            for when in TimeWrangler.datelist(year):
                archive_name = FileNameWrangler.archived(self, which, when)
                if not FileNameWrangler.archive_exists(self, archive_name):
                    self.download(which, when)
                if FileNameWrangler.archive_exists(self, archive_name):
                    self.expand(archive_name)

    def consume(self, which, when):
        """ Loads the data from the file for the given parameter. """
        fpath = FileNameWrangler.absolute_filepath(self, which, when)
        rio = rasterio.open(fpath, 'r')
        data = rio.read(1)
        rio.close()
        return data

    def store(self, data, out, when):
        """ Writes the data to an ArcGrid file """
        # DFMC_meta = VP3pm_tmp.meta.copy()
        profile = {}

        # ArcGrid
        with rasterio.open(FileNameWrangler.absolute_filepath(self, out, when), 'w', **profile) as dest:
            dest.write(data, 1)
            dest.close()
