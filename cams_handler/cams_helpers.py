''' Functions to get the observation time from data file.'''

import datetime as dt
import gdal

gdal.UseExceptions()

def timestamp_from_modis(filename):
    ds = gdal.Open(filename)
    metadata = ds.GetMetadata_Dict()
    timestr = metadata['RANGEBEGINNINGTIME']
    datestr = metadata['RANGEBEGINNINGDATE']
    filetime = dt.datetime.strptime(timestr, "%H:%M:%S.%f").time()
    filedate = dt.datetime.strptime(datestr, "%Y-%m-%d").date()
    return dt.datetime.combine(filedate, filetime)