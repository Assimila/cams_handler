from osgeo import gdal
import numpy as np
import datetime as dt
import CAMS_utils

gdal.UseExceptions()

def filename(tile, date, var):
    return CAMS_utils.vrt_filename(tile, date, var)

def scaled_data(band):
    ''' read data array from band an apply the scale and offset
    input:
        band,  an osgeo.gdal.Band
    returns:
        data, a numpy array of the correctly scaled band data.
    '''
    metadata = band.GetMetadata()
    scale = float(metadata['scale_factor'])
    offset = float(metadata['add_offset'])
    return (band.ReadAsArray() * scale + offset)
    return data
    
def convert_units(data, var):
    if var == 'tcwv':
        # source in kg m-2, want in g cm-2
        data = 0.1 * data
    if var == 'gtco3':
        # source in kg m-2, want in atm-cm
        data = data/2.1415e-2
    # All other variables returned unchanged.
    # AOD550 is unitless. sf is in m of water equivilent
    return data

def convertdatetime(netcdftime):
    ''' Convert the netcdf time from hours since 1900-01-01 00:00:0.0
    to a datetime object
    input:
        netcdftime date and time in hours since  1900-01-01 00:00:0.0
    output:
        date and time in datetime object
    '''
    origin = dt.datetime(1900,1,1,0,0,0) #netcdf times are hours since this time
    hours = dt.timedelta(hours=netcdftime)
    return origin + hours

def date_to_netcdf_time(datetime):
    ''' Convert a datetime object to the netcdf time in hours since 1900-01-01 00:00:0.0
    input:
        date and time in datetime object
    output:
        netcdftime date and time in hours since  1900-01-01 00:00:0.0
    '''
    origin = dt.datetime(1900,1,1,0,0,0) #netcdf times are hours since this time
    timedelta = datetime - origin
    hours = timedelta.total_seconds()/3600
    return hours

def get_timestamps(ds):
    ##############Not using this at present...
    times = ds.GetMetadata_Dict()['NETCDF_DIM_time_VALUES']
    # the metadata contains a string of comma separated values.
    # enclosed in curly braces.
    times = times[1:-1].split(',')
    datetimes = [convertdatetime(int(t)) for t in times]
    return datetimes

def get_banddata(ds, step, var):
    band = ds.GetRasterBand(step)
    banddata = scaled_data(band)
    return convert_units(banddata, var)

def get_var(fname, date, var):
    ds = gdal.Open(fname)

    # Get right timestep
    # Get timestamps from metadata
    times = ds.GetMetadataItem('NETCDF_DIM_time_VALUES')
    # Extract times from metadata string (in hours since midnight UTC, 1900,1,1)
    times = [int(t) for t in times[1:-1].split(",")]
    date_hours = date_to_netcdf_time(date)
    # Find data point closest in time to date
    nrst_index = (np.abs(np.array(times) - date_hours)).argmin()
    data_time = convertdatetime(times[nrst_index])
    #get data
    data = get_banddata(ds, nrst_index, var)
    #Get uncertanties
    return data, data_time

'''
    #loop through bands?
    data = np.zeros((ds.RasterCount, ds.RasterXSize, ds.RasterYSize))
    RasterCount = ds.RasterCount
    ds = None
    for i in xrange(RasterCount):
        ds = gdal.Open(fname)
        step = i+1 #gdal get raster band counts from 1, numpy from 0.
        data[i, ...] = get_banddata(ds, step, var)
        # read data
        #band = ds.GetRasterBand(step)
        #Data scale and offset
        #banddata = scaled_data(band)
        #band = None
        #convert units
        #data[i,...] = convert_units(banddata, var)
        #banddata = None
        datetimes = get_timestamps(ds)
        ds = None   # Close dataset to free up memory.
    return data, datetimes
'''

def read_cams(date, tile = 'h17v05'):
    '''
    Input:
        date - a datetime object with year, month, day, hours, minutes, seconds
        tile - modis tile reference eg h17v05
    Output:

    '''
    # Open file
    vars = CAMS_utils.parameters()
    data = {}
    times = {}
    for var in vars:
        print var
        fname = filename(tile, date, var) #need to make the file/date thing work...
        data[var], times[var] = get_var(fname, date, var)
    return data, times


def main():
    #startdate = dt.date(2016,1,1)
    #enddate = dt.date(2016, 3, 31)
    datetime = dt.datetime(2016, 2, 15, 10, 0, 0)
    tile = 'h17v05'
    #return read_cams(startdate, enddate, tile)
    return read_cams(datetime, tile)

if __name__ == "__main__":
    main()
