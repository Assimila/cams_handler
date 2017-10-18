""" Functions to get the observation time from data file."""

import datetime as dt
import gdal

gdal.UseExceptions()


def timestamp_from_modis(filename):
    """
    Read the observation time from a MODIS file.
    Works for MOD03 and MOD09 files. Not tested on anything else.
    :param filename: modis file name and location (e.g '/data/MOD03.A2017256.1115.006.2017257000928.hdf'
    :return: datetime object with start time and date of observation.
    """
    ds = gdal.Open(filename)
    metadata = ds.GetMetadata_Dict()
    try:
        timestr = metadata['RANGEBEGINNINGTIME']
        datestr = metadata['RANGEBEGINNINGDATE']
    except KeyError as e:
        raise("metadata RANGEBEGINNINGTIME and RANGEBEGINNINGDATE  not found in {}".format(filename), e)
    filetime = dt.datetime.strptime(timestr, "%H:%M:%S.%f").time()
    filedate = dt.datetime.strptime(datestr, "%Y-%m-%d").date()
    return dt.datetime.combine(filedate, filetime)
