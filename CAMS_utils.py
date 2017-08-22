from osgeo import gdal
import datetime as dt
import errno    
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def nc_filename(tile, year, month, directory='data', checkpath=True):
    path = os.path.join(directory, str(year))
    if checkpath:
        if not os.path.exists(path):
            mkdir_p(path)
    filename = os.path.join(path, "atmosvar_{tile}_{year}_{month}_fc.nc".format(
                                       tile=tile, year=year, month=month))
    return filename

def reproj_geotiff_filename(tile, year, month, var, directory='data', checkpath=True):
    path = os.path.join(directory, str(year))
    if checkpath:
        if not os.path.exists(path):
            mkdir_p(path)
    fname = os.path.join(path, "{var}_{tile}_{year}_{month}_sin_500m.tif".format(
                   var=var, tile=tile, year=year, month=month))
    return fname

def vrt_filename(tile, year, month, var, directory='data', checkpath=True):
    path = os.path.join(directory, str(year))
    if checkpath:
        if not os.path.exists(path):
            mkdir_p(path)
    fname = os.path.join(path, "{var}_{tile}_{year}_{month}_sin_500m.vrt".format(
                   var=var, tile=tile, year=year, month=month))
    return fname

def parameters():
    return ['tcwv', 'gtco3', 'aod550', 'sf']

def get_tile_extent(MOD09band):
    ds = gdal.Open(MOD09band)
    (xmin, xres, xrot, ymax, yrot, yres) = ds.GetGeoTransform()
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    ds = None
    xmax = xmin + xsize * xres
    ymin = ymax + ysize * yres
    return  xmin, xmax, xres, ymin, ymax, yres
