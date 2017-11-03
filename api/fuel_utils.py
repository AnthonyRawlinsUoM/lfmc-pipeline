import os
import os.path

from datetime import datetime
import pandas as pd


class TimeWrangler:
    def __init__(self):
        self.a = 0

    def yearslist(self, f, l):
        yl = []
        for r in range(f.year, l.year):
            yl.append(r)
        return yl

    def datelist(self, year):
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 26)  # BOM Christmas shutdown?? Not sure why happens in every dataset!
        return pd.to_datetime(pd.date_range(start, end, freq='D').tolist())


class FileNameWrangler:
    def __init__(self, model):

        self.params = model.get_parameters()
        self.outputs = model.get_outputs()

    def construct(self, which, when):
        return self.params[which]['prefix'] + "_" + when.strftime("%Y%m%d") + self.params[which]['suffix']

    def archived(self, which, when):
        return self.construct(which, when) + self.params[which]['compression suffix']

    def ensure_dir(self, which):
        directory = os.path.dirname(self.params[which]['path'])
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True

    def archive_exists(self, which):
        self.ensure_dir(which)
        return os.path.isfile(self.archived(which))

    def file_exists(self, fpath):
        return os.path.isfile(fpath)

    def url(self, which, when):
        return self.params[which]['url'] + self.awap_name(which, when)

    def path(self, which):
        return self.params[which]['path']

    def absolute_path(self, which):
        return self.path(which)

    def absolute_filepath(self, which, when):
        return self.path(which) + self.construct(which,when)

    def awap_name(self, which, when):
        return when.strftime("%Y%m%d") + when.strftime("%Y%m%d") + self.params[which]['suffix'] +self.params[which]['compression_suffix']