from osgeo import gdal
import datetime as dt

def nc_filename(tile, startdate, enddate):
    return  "atmosvar_{tile}_{startd}_{endd}_fc.nc".format(
                   tile=tile, startd=startdate, endd=enddate)

def reproj_geotiff_filename(tile, startdate, enddate, var):
    fname = '{var}_{tile}_{startd}_{endd}_sin_500m.tif'.format(
                   var=var, tile=tile, startd=startdate, endd=enddate)
    return fname

def vrt_filename(tile, date, var):
    # TODO: need to choose a convention and extract filename from date
    startdate = dt.date(2016,1,1)
    enddate = dt.date(2016, 3, 31)
    fname = '{var}_{tile}_{startd}_{endd}_sin_500m.vrt'.format(
                   var=var, tile=tile, startd=startdate, endd=enddate)
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
