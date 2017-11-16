import os
import os.path

from datetime import datetime
import pandas as pd


class TimeWrangler:
    @staticmethod
    def yearslist(f, l):
        start = datetime(f, 1, 1)
        end = datetime(l, 1, 1)

        # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
        return pd.to_datetime(pd.date_range(start, end, freq='A').tolist())

    @staticmethod
    def datelist(for_year: int) -> list:
        start = datetime(for_year, 1, 1)
        end = datetime(for_year, 12, 26)  # BOM Christmas shutdown?? Not sure why happens in every dataset!
        return pd.to_datetime(pd.date_range(start, end, freq='D').tolist())

    pass


class FileNameWrangler:
    @staticmethod
    def construct(model, which, when):
        return model.parameters[which]['prefix'] + "_" + \
               when.strftime("%Y%m%d") + \
               model.parameters[which]['suffix']

    @staticmethod
    def archived(model, which, when):
        return model.parameters[which]['prefix'] + "_" + \
               when.strftime("%Y%m%d") + \
               model.parameters[which]['suffix'] + \
               model.parameters[which]['compression_suffix']

    @staticmethod
    def ensure_dir(model, which):
        directory = os.path.dirname(model.parameters[which]['path'])
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True

    @staticmethod
    def archive_exists(model, which, when):
        return os.path.isfile(model.parameters[which]['prefix'] + "_" +
                              when.strftime("%Y%m%d") +
                              model.parameters[which]['suffix'] +
                              model.parameters[which]['compression_suffix'])

    @staticmethod
    def file_exists(fpath):
        return os.path.isfile(fpath)

    @staticmethod
    def url(model, which, when):
        return model.parameters[which]['url'] + \
               when.strftime("%Y%m%d") + \
               when.strftime("%Y%m%d") + \
               model.parameters[which]['suffix'] + \
               model.parameters[which]['compression_suffix']

    @staticmethod
    def path(model, which):
        return model.parameters[which]['path']

    @staticmethod
    def absolute_file_path(model, which, when):
        print(model)

        f_path = model.parameters[which]['path'] + \
                 model.parameters[which]['prefix'] + "_" + \
                 when.strftime("%Y%m%d") + \
                 model.parameters[which]['suffix']
        print(f_path)
        return f_path

    @staticmethod
    def awap_name(model, which, when):
        return when.strftime("%Y%m%d") + \
               when.strftime("%Y%m%d") + \
               model.parameters[which]['suffix'] + \
               model.parameters[which]['compression_suffix']

    pass
