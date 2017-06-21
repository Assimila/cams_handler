import gdal
import numpy as np

gdal.UseExceptions()

def filename(tile, var):
    fname = '{var}_{tile}_sin_500m.tif'.format(var=var, tile=tile)
    return fname

def scaled_data(band):
    ''' read data array from band an apply the scale and offset'''
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
    #All other variables returned unchanged.
    return data

def get_var(tile, var):
    fname = filename(tile, var)
    ds = gdal.Open(fname)
    #loop through bands?
    data = np.zeros((ds.RasterCount, ds.RasterXSize, ds.RasterYSize))
    for i in xrange(ds.RasterCount):
        step = i+1
        # read data
        band = ds.GetRasterBand(step)
        #Data scale and offset
        banddata = scaled_data(band)
        #convert units
        data[i,...] = convert_units(banddata, var)
    return data

def read_cams(tile = 'h17v03'):
    # Open file
    vars = ['tcwv', 'gtco3']
    data = {}
    for var in vars:
        print var
        data[var] = get_var(tile, var)
    return data


def main():
    return read_cams()

if __name__ == "__main__":
    main()
