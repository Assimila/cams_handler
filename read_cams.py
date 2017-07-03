import gdal
import numpy as np
import datetime as dt
import CAMS_utils

gdal.UseExceptions()

def filename(tile, var):
    return CAMS_utils.reproj_geotiff_filename(tile, var)

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

def get_timestamps(ds):
    times = ds.GetMetadata_Dict()['NETCDF_DIM_time_VALUES']
    # the metadata contains a string of comma separated values.
    # enclosed in curly braces.
    times = times[1:-1].split(',')
    datetimes = [convertdatetime(int(t)) for t in times]
    return datetimes

def get_var(tile, var):
    fname = filename(tile, var)
    ds = gdal.Open(fname)
    #loop through bands?
    data = np.zeros((ds.RasterCount, ds.RasterXSize, ds.RasterYSize))
    for i in xrange(ds.RasterCount):
        step = i+1 #gdal get raster band counts from 1, numpy from 0.
        # read data
        band = ds.GetRasterBand(step)
        #Data scale and offset
        banddata = scaled_data(band)
        #convert units
        data[i,...] = convert_units(banddata, var)
    datetimes = get_timestamps(ds)
    return data, datetimes

def read_cams(tile = 'h17v05'):
    # Open file
    vars = CAMS_utils.parameters()
    data = {}
    times = {}
    for var in vars:
        print var
        data[var], times[var] = get_var(tile, var)
    return data, times


def main():
    return read_cams()

if __name__ == "__main__":
    main()
