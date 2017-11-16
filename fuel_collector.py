#!/home/anthonyrawlins/anaconda3/bin/python3

from abc import abstractmethod
import urllib.request
from urllib.error import URLError
import subprocess
import rasterio
import multiprocessing
from fuel_utils import FileNameWrangler, TimeWrangler


class Collector(FileNameWrangler, TimeWrangler):

    def download(self, model, which, when):
        """Downloads and extracts data from BOM based on date range"""
        what = FileNameWrangler.url(model, which, when)
        where = FileNameWrangler.absolute_file_path(model, which, when)

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

    @staticmethod
    def expand(fpath):
        """ OS level decompression algorithm; spawns a subprocess. """
        subprocess.run(["uncompress", "-k", fpath, "/dev/null"], stdout=subprocess.PIPE)

    @abstractmethod
    def collect(self, year):
        return None

    @staticmethod
    def consume(model, param, when):
        """ Loads the data from the file for the given parameter. """
        f_path = FileNameWrangler.absolute_file_path(model, param, when)
        rio = rasterio.open(f_path, 'r')
        data = rio.read(1)
        rio.close()
        return data

    pass
