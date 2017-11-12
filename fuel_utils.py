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

    def construct(self, model, which, when):
        return model.get_parameters(which)['prefix'] + "_" +\
               when.strftime("%Y%m%d") +\
               model.get_parameters(which)['suffix']

    def archived(self, model, which, when):
        return self.construct(model, which, when) +\
               model.get_parameters(which)['compression suffix']

    def ensure_dir(self, model, which):
        directory = os.path.dirname(model.get_parameters(which)['path'])
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True

    def archive_exists(self, model, which):
        self.ensure_dir(model, which)
        return os.path.isfile(self.archived(model, which))

    def file_exists(self, fpath):
        return os.path.isfile(fpath)

    def url(self, model, which, when):
        return model.get_parameters(which)['url'] +\
               self.awap_name(model, which, when)

    def path(self, model, which):
        return model.get_parameters(which)['path']

    def absolute_path(self, which):
        return self.path(which)

    def absolute_filepath(self, model, which, when):
        return self.path(model, which) + self.construct(model, which, when)

    def awap_name(self, model, which, when):
        return when.strftime("%Y%m%d") +\
               when.strftime("%Y%m%d") +\
               model.get_parameters(which)['suffix'] +\
               model.get_parameters(which)['compression_suffix']