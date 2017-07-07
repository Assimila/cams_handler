import gdal

def nc_filename(tile, start, end):
    return  "atmosvar_{tile}_{start}_{end}_fc.nc".format(tile=tile, start=start, end=end)

def reproj_geotiff_filename(tile, var):
    fname = '{var}_{tile}_sin_500m.tif'.format(var=var, tile=tile)
    return fname

def parameters():
    return ['tcwv', 'gtco3', 'aod550', 'sf']

def get_tile_extent(MOD09band):
    ds = gdal.Open(MOD09band)
    (xmin, xres, xrot, ymax, yrot, yres) = ds.GetGeoTransform()
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    xmax = xmin + xsize * xres
    ymin = ymax + ysize * yres
    return  xmin, xmax, xres, ymin, ymax, yres
