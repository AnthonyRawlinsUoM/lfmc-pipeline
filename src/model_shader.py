import datashader as ds
from datashader import transfer_functions as tf

# TODO Colormap as viridis
from matplotlib import viridis

from datashader.colors import Greys9
Greys9_r = list(reversed(Greys9))[:2-]

import pandas as pd
import numpy as np
import ncdf4
import os

# Weather Data
weatherPath = '/media/anthonyrawlins/Archives/Weather/'

allWeather = os.listdir(weatherPath)

temperatureFile = 'IDV71000_VIC_T_SFC.nc'
windMagFile = 'IDV71006_VIC_Wind_Mag_SFC.nc'
windDirFile = 'IDV71089_VIC_Wind_Dir_SFC.nc'
skyFile = 'IDV71017_VIC_Sky_SFC.nc'
humidityFile = 'IDV71018_VIC_RH_SFC.nc'
droughtFactorFile = 'IDV71127_VIC_DF_SFC.nc'

files = [temperatureFile, windMagFile, windDirFile, skyFile, humidityFile, droughtFactorFile]

for (path in allWeather):
    for(f in files):
        dfile = join(path,f)
        if(os.path.isfile(dfile)):
            rootgrp = Dataset(, "w", format="NETCDF4")
            print(rootgrp.data_model)
            rootgrp.close()

# For the victorian region bounds...

# TODO - render for each zoom level
#
# df is a DataFrame-like Object
%time
cvs = ds.Canvas(plot_width=plot_width, plot_height=plot_height, x_range, y_range)
agg = cvs.points(df, 'lat', 'lng', ds.mean('fuel_moisture'))
img = tf.interpolate(agg, cmap=viridis, how='linear')

# TODO - upload the image to GeoServer REST API
