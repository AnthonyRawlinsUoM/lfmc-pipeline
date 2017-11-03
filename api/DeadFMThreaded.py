
# coding: utf-8

# # Dead Fuel Moisture Model
#
# ### Nolan et al.

# Numeric
import pandas as pd
import numpy as np

# OS & Web
import urllib.request
import subprocess
import os
import os.path
import argparse
import fnmatch
from urllib.request import Request, urlopen
from urllib.error import URLError

# Formats & Plotting
import json
from json_tricks.np import dump, dumps, load, loads, strip_comments
import rasterio
import gdal
import ogr
import osr
import netCDF4 as nc4
import matplotlib.pyplot as plt
import pyproj as proj
import matplotlib
from matplotlib import cm

# Date
from datetime import datetime, timedelta
from IPython.display import display

# Multi-threading
import multiprocessing


# ## Environment Paths & Configuration

PROJECT_ROOT = "/home/anthonyrawlins/Data/DEAD_FM/"
CLIMATE_STORE = PROJECT_ROOT + "Climate/"
AWAP_PATH = CLIMATE_STORE + "AWAP/"
AWAP_DAILY_PATH = AWAP_PATH + "AWAP_Daily/"
DFMC_PATH = CLIMATE_STORE + "DFMC/Daily/"


def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)


ensure_dir(PROJECT_ROOT)
ensure_dir(CLIMATE_STORE)
ensure_dir(AWAP_PATH)
ensure_dir(AWAP_DAILY_PATH)
ensure_dir(DFMC_PATH)


# ## BOM File naming conventions and URLs

# BOM File naming conventions
# Prefixes
vapour_prefix = 'VP3pm'
temp_prefix = 'Tmx'
precip_prefix = 'P'
DFMC_prefix = 'DFMC'
compression_suffix = '.Z'
suffix = '.grid'

# BOM Daily Data Access Paths
vapour_url = "http://www.bom.gov.au/web03/ncc/www/awap/vprp/vprph15/daily/grid/0.05/history/nat/"
max_avg_temp_url = "http://www.bom.gov.au/web03/ncc/www/awap/temperature/maxave/daily/grid/0.05/history/nat/"
precipitation_url = "http://www.bom.gov.au/web03/ncc/www/awap/rainfall/totals/daily/grid/0.05/history/nat/"

vapour_path = AWAP_DAILY_PATH + vapour_prefix + "/"
max_avg_temp_path = AWAP_DAILY_PATH + temp_prefix + "/"
precipitation_path = AWAP_DAILY_PATH + precip_prefix + "/"

# Required Params for the Model
parameters = [
	{
		'path': vapour_path,
		'url': vapour_url,
		'prefix': vapour_prefix
	},
	{
		'path': max_avg_temp_path,
		'url': max_avg_temp_url,
		'prefix': temp_prefix
	},
	{
		'path': precipitation_path,
		'url': precipitation_url,
		'prefix': precip_prefix
	}
]

# Colormap choice
viridis = plt.cm.viridis_r
greys = plt.get_cmap('Greys')


def plotlySetup():
	magma_cmap = matplotlib.cm.get_cmap('magma')
	viridis_cmap = matplotlib.cm.get_cmap('viridis')

	viridis_rgb = []
	magma_rgb = []
	norm = matplotlib.colors.Normalize(vmin=0, vmax=255)

	for i in range(0, 255):
		k = matplotlib.colors.colorConverter.to_rgb(magma_cmap(norm(i)))
		magma_rgb.append(k)

	for i in range(0, 255):
		k = matplotlib.colors.colorConverter.to_rgb(viridis_cmap(norm(i)))
		viridis_rgb.append(k)
	magma_plotly = matplotlib_to_plotly(magma_cmap, 255)
	viridis_plotly = matplotlib_to_plotly(viridis_cmap, 255)


# ## Utility Functions
 # Using GDA94 (GeoScience Australia)
gda94 = proj.Proj(init='epsg:4283')


def pixelCoordsFromMapCoords(lng, lat):
	x, y = gda94(lng, lat)
	return pixelCoords(x, y)


def pixelCoords(x, y):
	xf = 886 / (2.7053 - 1.8850)
	yf = 691 / (-0.7854 - -0.1745)
	px = (2.7053 - x) * xf
	py = (y - -0.1745) * yf
	return int(px), int(py)


def testSetup():
	print('\nTop-left:')
	x, y = gda94(155.0000, -10.0000)
	print('x =%14.4f y =%11.4f' % (x, y))
	lng, lat = gda94(x, y, inverse=True)
	print('lng =%11.4f lat =%11.4f' % (lng, lat))
	print(pixelCoords(x, y))

	print('\nTop-right:')
	x, y = gda94(108.0000, -10.0000)
	print('x =%14.4f y =%11.4f' % (x, y))
	lng, lat = gda94(x, y, inverse=True)
	print('lng =%11.4f lat =%11.4f' % (lng, lat))
	print(pixelCoords(x, y))

	print('\nBottom-left:')
	x, y = gda94(155.0000, -45.0000)
	print('x =%14.4f y =%11.4f' % (x, y))
	lng, lat = gda94(x, y, inverse=True)
	print('lng =%11.4f lat =%11.4f' % (lng, lat))
	print(pixelCoords(x, y))

	print('\nBottom-right:')
	x, y = gda94(108.0000, -45.0000)
	print('x =%14.4f y =%11.4f' % (x, y))
	lng, lat = gda94(x, y, inverse=True)
	print('lng =%11.4f lat =%11.4f' % (lng, lat))
	print(pixelCoords(x, y))

# DEBUG...
# testSetup()


def bomFilename(d):
	return d.strftime("%Y%m%d") + d.strftime("%Y%m%d") + suffix + compression_suffix


def constructFilename(prefix, suffix, start):
	return prefix + "_" + start.strftime("%Y%m%d") + suffix


def uncompressedFilename(filename):
	if filename.endswith('.Z'):
		return filename[:-2]
	return filename


def checkCache(filepath, d):
	f = path + constructFilename(d)
	# print('Checking if ' + f + ', exists...')
	if os.path.isfile(f):
		# print('Yes')
		return true
	else:
		# print('No')
		return false


# ## Data Access Functions

def downloadFromBOM(url, path, savefile, date):
	'''Downloads and extracts data from BOM based on date range'''
	inputfile = bomFilename(date)
	# print(">>> Downloading: " + url + inputfile)

	try:
		response = urllib.request.urlretrieve(url + inputfile, path + savefile)
	except URLError as e:
		if hasattr(e, 'reason'):
			print('We failed to reach a server.')
			print('Reason: ', e.reason)
		elif hasattr(e, 'code'):
			print('The server couldn\'t fulfill the request.')
			print('Error code: ', e.code)
	# else:
		# everything is fine
		# print('Download complete')


def expandArchiveFile(path, file):
	# print("Expanding: " + path + file)
	complete = subprocess.run(
		["uncompress", "-k", path + file, "/dev/null"], stdout=subprocess.PIPE)


def DFMC_RetrieveDataForDate(d):
	# Don't re-download data from BOM,
	# but DO retrieve data for dates that we don't have

	# For Vapour pressure, Temp, and Precip
	for params in parameters:
		# Reconstruct file names and paths
		archive_file = constructFilename(
			params['prefix'], suffix + compression_suffix, d)
		grid_file = constructFilename(params['prefix'], suffix, d)

		# Does a grid exist?
		# print('Checking if ' + params['path'] + archive_file + ', exists...')
		if not os.path.isfile(params['path'] + grid_file):
		# No - doesn't exist
			#print('> No, checking for archive')
			# Does the archive exist?
			if not os.path.isfile(params['path'] + archive_file):
				# No - download it
				# print('>> No, no archive exists...')
				downloadFromBOM(params['url'], params['path'], archive_file, d)
			# else:
				# Yes - exists.
				# print('>> Archived Data for ' + d.strftime("%Y%m%d") + ' already exists in ' + params['path'] + '. Not downloading.')

		# Now expand it...
		expandArchiveFile(params['path'], archive_file)
		# else:
		# print('> Yes, cached grid exists for ' + d.strftime("%Y%m%d") + ', in file: ' + grid_file)
		# Yes - no action necessary

	# # API


def DFMC_Calculate(date):

	DFMC_filename = constructFilename(DFMC_prefix, '.grid', date)
	P_filename = constructFilename(precip_prefix, '.grid', date)

	# load the file using rasterio
	VP3pm_filename = constructFilename(vapour_prefix, suffix, date)
	VP3pm_tmp = rasterio.open(vapour_path + VP3pm_filename, 'r')
	VP3pm_im = VP3pm_tmp.read(1)

	# Normalization...
	# VP3pm_norm = plt.Normalize(vmin=VP3pm_im.min(), vmax=VP3pm_im.max())
	# VP3pm_image = cmap(VP3pm_norm(VP3pm_im))

	# OPTION - Save color plots for later use...
	# plot = vapour_path+VP3pm_filename+'.png'

	# if not os.path.isfile(plot):
	#	plt.title(VP3pm_filename)
	#	plt.imsave(vapour_path+VP3pm_filename+'.png', VP3pm_im)
	#	plt.imshow(VP3pm_image, cmap)
	#	plt.show()

	# in hPa from AWAP, so multiply by 0.1 to convert to KPa
	ea_tmp2 = VP3pm_im * 0.1

	Tmx_filename = constructFilename(temp_prefix, '.grid', date)
	Tmx_tmp = rasterio.open(max_avg_temp_path + Tmx_filename, 'r')
	Tmx_im = Tmx_tmp.read(1)

	# Normalization...
	# Tmx_norm = plt.Normalize(vmin=Tmx_im.min(), vmax=Tmx_im.max())
	# Tmx_image = cmap(Tmx_norm(Tmx_im))

	# OPTION - Save color plots for later use...
	# plt.imsave(max_avg_temp_path+Tmx_filename+'.png', Tmx_im)
	# plt.title(max_avg_temp_path + Tmx_filename)
	# plt.imshow(Tmx_image, cmap)
	# plt.show()

	# From daily mean temperature (T) we can compute saturation vapour pressure:
	es_tmp = 0.6108 * np.exp(17.27 * Tmx_im / (Tmx_im + 237.3))# In KPa!!

	# ...and VPD in KPa, constrain to 0 when calculated RH >100%
	# Switch commented lines to activate clipping/clamping

	# CLAMPING OFF!!!!
	D_tmp = np.clip(ea_tmp2 - es_tmp, None, 0)
	#		D_tmp = np.clip(ea_tmp2 - es_tmp, 0, None)
	#		D_tmp = ea_tmp2 - es_tmp

	# compute DFMC (%)
	# DFMC model (Resco et al., AFM 2016) with the calibration coefficients for SE Australia from Nolan et al. 2016. (RSE)
	# DFMCfun <- function(x) {
	#y <- 6.79+27.43*exp(1.05*x)
	#return(y)}
	DFMC_tmp = 6.79 + (27.43 * np.exp(1.05 * D_tmp))
	# DFMC_summary = pd.DataFrame(DFMC_tmp)
	# print(DFMC_summary.describe())

	# save the image

	# plt.title(DFMC_PATH+DFMC_filename)
	# DFMC_norm = plt.Normalize(vmin=DFMC_tmp.min(), vmax=DFMC_tmp.max())
	# DFMC_image = cmap(DFMC_norm(DFMC_tmp))
	DFMC_image = viridis(DFMC_tmp)
	DFMC_meta = VP3pm_tmp.meta.copy()

	# ArcGrid
	with rasterio.open(DFMC_PATH + DFMC_filename, 'w', **DFMC_meta) as dest:
		dest.write(DFMC_tmp, 1)
		dest.close()

	# 32bit per pixel to 8bit per pixel conversion
	DFMC_image = DFMC_tmp.real.astype(rasterio.uint8)

	#GeoTIFF
	DFMC_meta['driver'] = "GEOTIFF"
	DFMC_meta['photometric'] = "RGB"
	with rasterio.open(DFMC_PATH + DFMC_filename+'.plot.tiff', 'w', **DFMC_meta) as dest:
		dest.write(DFMC_image, indexes=1)
		dest.write_colormap(
			1, {
				0: (255, 0, 0, 255),
				255: (0, 0, 255, 255) })
		dest.close()

	# PNG
	plt.imsave(DFMC_PATH + DFMC_filename + '.8bit.tif',
				 DFMC_tmp, cmap=plt.cm.viridis_r)

	# plt.imshow(DFMC_tmp, cmap=plt.cm.viridis_r)
	# plt.show()

	P_tmp = rasterio.open(precipitation_path + P_filename, 'r')
	P_im = P_tmp.read(1)

	# P_norm = plt.Normalize(vmin=P_im.min(), vmax=P_im.max())
	# P_image = cmap(P_norm(P_im))
	# plt.imsave(precipitation_path+P_filename+'.tif', P_im)
	return DFMC_tmp


def DFMC_TimeSeriesAtPoint(lng, lat, datelist):

	tolerance = 0.06
	v = -999999
	vmin = -999999
	vmax = -999999
	ts = []
	res = {}
	res['meta'] = {
		"lat": lat,
		"lng": lng,
		"start": datelist[0].strftime("%Y-%m-%dT15:00:00.000Z"),
		"finish": datelist[len(datelist) - 1].strftime("%Y-%m-%dT15:00:00.000Z"),
		"rainfall": "Expressed as percentage gain in water saturation",
		"spatial_resolution": "0.05 degrees",
		"temporal_granularity": "24 hours"
	}

	x, y = pixelCoordsFromMapCoords(lng, lat)

	# If no 3D File try Database

	if ndarr[0, 0, 0] > 0:
		vts = ndarr[x, y, :]

		for i, v in enumerate(vts):
			vmin = max(v - (v * tolerance), i)
			vmax = v + (v * tolerance)
			ts.append({
				"name": datelist[i].strftime("%Y-%m-%dT15:00:00.000Z"),
				"value": v,
				"min": v,
				"max": v,
				"rainfall": 0.0,

			})
	else:
		# Try to multithread the date/data collection
		pool = multiprocessing.Pool(processes=12)
		output = pool.map(DFMC_OnDate, datelist)
		# If no Database reconstruct from grid files
		for i, date in enumerate(datelist):
			# retrieves data required for calc from file and/or urls as req.

			DFMC_filename = constructFilename(DFMC_prefix, '.grid', date)
			# print('Loading dfmc for time #' + str(i) +
			#		'from ' + DFMC_PATH + DFMC_filename)
			try:
				r = rasterio.open(DFMC_PATH + DFMC_filename, 'r')
				image = r.read(1)
				ndarr[:, :, i] = image
				v = image[y, x]
			except Exception as e:
				raise

		 	# print('# Value @ (' + str(x) + ',' + str(y) + '), on ' +
			#		date.strftime("%d/%m/%Y") + ': ' + str(v) + '[' + str(type(v)) + ']')
			if i == len(datelist)-1:
				vmin = 0
				vmax = 100
			else:
				vmin = max(v - (v * tolerance), 0)
				vmax = v + (v * tolerance)
				# precip = 0.0

			ts.append({
				"name": date.strftime("%Y-%m-%dT15:00:00.000Z"),
				"value": v,
				"min": vmin,
				"max": vmax,
				"rainfall": 0.0,
			})
			r.close()

	res['series'] = ts
	res['name'] = "Nolan Dead Fuel Moisture"
	return res


def DFMC_CompleteMapForDate(date):
	# STUB!
	return null


def DFMC_OnDate(date):
	'''With the date appropriate file in the Tmx, VP3pm, and P folder: calculate the DFMC at a specific lat/lng'''

	DFMC_filename = constructFilename(DFMC_prefix, '.grid', date)
	P_filename = constructFilename(precip_prefix, '.grid', date)

	# First, check if the dfmc file exists for that date
	if not os.path.isfile(DFMC_PATH + DFMC_filename):
		# print('No DFMC for ' + date.strftime("%d/%m/%Y") + '. Calculating...')

		# Ensure we have the data we need for the date in question
		try:
			DFMC_RetrieveDataForDate(date)
			DFMC_Calculate(date)
		except Exception as e:
			print(e)
			exit(-1)

	# else:
		# print('DFMC Data exists for ' + date.strftime("%d/%m/%Y") + '. Retrieving...')

		return True


def DFMC_TimeIndexToDate(s):
	'''Maps a TimeIndex to an exact date'''
	return None


def DFMC_DateToTimeIndex(d):
	''' Maps a date object to a TimeIndex'''
	return None


def DFMC_DateRangeToTimeIndexRange(start, end):
	''' Maps an exact list of dates to a range of TimeIndices'''
	return s, e


def DFMC_TimeIndexRangeToDateRange(s, e):
	''' Maps TimeIndex eg., 0-365 (by default) to exact range of dates.'''
	return start, end


def DFMC_AtPointOnDate(location, date):
	'''With the date appropriate file in the Tmx, VP3pm, and P folder: calculate the DFMC and precipitation at a specific lat/lng'''

	DFMC_filename = constructFilename(DFMC_prefix, '.grid', date)
	P_filename = constructFilename(precip_prefix, '.grid', date)

	# First, check if the dfmc file exists for that date
	if not os.path.isfile(DFMC_PATH + DFMC_filename):
		# print('No DFMC for ' + date.strftime("%d/%m/%Y") + '. Calculating...')

		# Ensure we have the data we need for the date in question
		DFMC_RetrieveDataForDate(date)
		DFMC_Calculate(date)
	# else:
		# print('DFMC Data exists for ' + date.strftime("%d/%m/%Y") + '. Retrieving...')

	# Calculate xy coords from latlng

	# Hard-coded value for testing...
	#(725,530)
	dfmc_value = 0

	dfmcgrid = rasterio.open(DFMC_PATH + DFMC_filename, 'r').read(1)
	pgrid = rasterio.open(precipitation_path + P_filename, 'r').read(1)

	# Retrieve point value
	dfmc_value = dfmcgrid[location['y']][location['x']]
	p_value = pgrid[location['y']][location['x']]

	return (dfmc_value, p_value)


# ## Experiment Configuration Options
#
# Includes date range. This will be replaced by parameters from the API call.

# Date Range
def testDateRange():
	days_history = 365
	end = datetime(2017, 10, 22)
	datelist = pd.to_datetime(pd.date_range(
		end - timedelta(days=days_history), periods=days_history, freq='D').tolist())

# # Testing & validation


def testConfig():
	testpoint = {'lng': 148.46965883976816, 'lat': -39.67518078987623}
	dfmc_test = DFMC_TimeSeriesAtPoint(
		testpoint['lng'], testpoint['lat'], datelist)
	print(dumps(dfmc_test))


def writeNetCDF4(data):
	#	 lon = data[:,,]
	#	 lat = data[,:,]
	#	 z = data[,,:]

	f = nc4.Dataset(DFMC_PATH + 'dfmc.nc', 'w',
					format='NETCDF4')# 'w' stands for write
	tempgrp = f.createGroup('DFMC_data')
	tempgrp.createDimension('lon', len(lon))
	tempgrp.createDimension('lat', len(lat))
	tempgrp.createDimension('z', len(z))
	tempgrp.createDimension('time', None)

	longitude = tempgrp.createVariable('Longitude', 'f4', 'lon')
	latitude = tempgrp.createVariable('Latitude', 'f4', 'lat')
	readings = tempgrp.createVariable('Levels', 'i4', 'z')
	moist = tempgrp.createVariable(
		'Dead Fuel Moisture', 'f4', ('time', 'lon', 'lat', 'z'))
	time = tempgrp.createVariable('Time', 'i4', 'time')

	longitude[:] = lon
	latitude[:] = lat
	levels[:] = z
	moist[0, :, :, :] = temp_data

	# Add global attributes
	f.description = "Example dataset containing one group moisture values by Dead Fuel Moisture Content Model (Nolan et al.)"
	f.history = "Created " + today.strftime("%d/%m/%y")

	# Add local attributes to variable instances
	longitude.units = 'Degrees East'
	latitude.units = 'Degrees South'
	time.units = 'Days since Jan 01, 0001'
	moist.units = '% water by weight'
	readings.units = '% water by weight'


def matplotlib_to_plotly(cmap, pl_entries):
	h = 1.0 / (pl_entries - 1)
	pl_colorscale = []

	for k in range(pl_entries):
		C = list(map(np.uint8, np.array(cmap(k * h)[:3]) * 255))
		pl_colorscale.append([k * h, 'rgb' + str((C[0], C[1], C[2]))])

	return pl_colorscale


def get_data(t):
	brushsize = 300

	startx = 0
	starty = 0
	startz = 0

	xrange = 885
	yrange = 690
	timerange = 1

	endx = startx + xrange
	endy = starty + yrange
	endz = startz + timerange

	cache = ndarr[starty:endy, startx:endx, startz:endz]
	# cache = ndarr[:,:,0]
	# cache.reshape(1,886,691)
	# print(cache.shape)
	# print(cache)

	data = [
		go.Surface(
			z=cache[:, :, 0],
			colorscale=viridis
		)
	]
	return data


ndarr = np.zeros((691, 886, 1), dtype=np.float32)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-v", "--verbose", help="increase output verbosity", action="store_true")
	parser.add_argument("lng", help="longitude of the point to be retrieved")
	parser.add_argument("lat", help="latitude of the point to be retrieved")
	parser.add_argument(
		"start", help="starting date YYYYMMDD of the search range")
	parser.add_argument("end", help="ending date YYYYMMDD of the search range")
	args = parser.parse_args()

	if args.verbose:
		print("verbosity turned on")

	start = datetime.strptime(args.start, "%Y%m%d")
	end = datetime.strptime(args.end, "%Y%m%d")
	lat = float(args.lat)
	lng = float(args.lng)

	datelist = pd.to_datetime(pd.date_range(
		start=start, end=end, freq='D').tolist())
	days_history = (end - start).days + 1

	# load the 3D Array for a Year's History
	global ndarr
	ndarr = np.zeros((691, 886, days_history), dtype=np.float32)
	print(dumps(DFMC_TimeSeriesAtPoint(lng, lat, datelist)))


if __name__ == '__main__':
	main()
