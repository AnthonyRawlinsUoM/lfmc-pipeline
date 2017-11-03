#!/home/anthonyrawlins/anaconda3/bin/python3
import abc
import netCDF4 as nc4


class Driver:

    def __init__(self):
        self.data = []

    @abc.abstractmethod
    def load(self, when):
        """ Load and return the data for when """

    @abc.abstractmethod
    def save(self, data, where):
        """ Default driver can't save your data. Use a subclass! """


class NetCDF4Driver(Driver):
    def __init__(self, path, prefix):
        self.path = path
        self.prefix = prefix
        self.extension = ".nc"
        self.time_units = 'days since 2017-01-01 00:00:00'

    def load(self, when):
        print("Attempting to load NetCDF file for: " + str(when))
        file_path = self.path + str(when) + "_" + self.prefix.lower() + self.extension
        print("...from: " + file_path)
        root_group = nc4.Dataset(file_path, 'r', format='NETCDF4')

        for children in self.walktree(root_group):
            for child in children:
                print(child)

        nd = root_group.groups['DFMC_data']['Dead Fuel Moisture'][:, :, :, 0]

        return nd

    def recreate_datetime(self, f):
        return nc4.num2date(f, units=self.time_units, calendar='standard')

    def get_time_indexes(self, datetime_list):
        return nc4.date2index(datetime_list, self.load[:, 0, 0])

    def walktree(self, top):
        values = top.groups.values()
        yield values
        for value in top.groups.values():
            for children in self.walktree(value):
                yield children

    def save(self, data, where):
        t = data[:, 0, 0]
        lon = data[0, :, 0]
        lat = data[0, 0, :]

        root_group = nc4.Dataset(where + self.extension, 'w', format='NETCDF4')

        fuel_grp = root_group.createGroup('DFMC_data')

        fuel_grp.createDimension('lon', len(lon))
        fuel_grp.createDimension('lat', len(lat))
        fuel_grp.createDimension('time', len(t))
        fuel_grp.createDimension('z', 1)

        longitude = fuel_grp.createVariable('Longitude', 'f4', 'lon')
        latitude = fuel_grp.createVariable('Latitude', 'f4', 'lat')
        time = fuel_grp.createVariable('Time', 'f4', 'time')
        z = fuel_grp.createVariable('Z', 'i4', 'z')

        moist = fuel_grp.createVariable('DeadFuelMoisture', 'f4', ('time', 'lon', 'lat', 'z'))

        longitude[:] = lon
        latitude[:] = lat  # reverse to flip y axis back right way up?
        moist[:, :, :, 0] = data

        # Add global attributes
        root_group.description = "Example dataset containing one group moisture values by Dead Fuel Moisture Content Model (Nolan et al.)"
        # f.history = "Created " + today.strftime("%d/%m/%y")

        # Add local attributes to variable instances
        longitude.units = 'Degrees East'
        latitude.units = 'Degrees South'
        time.units = 'Days since Jan 01, 0001'
        moist.units = '% water by weight'

        root_group.close()
