
def nc_filename(tile):
    return  "atmosvar_fc.nc"

def reproj_geotiff_filename(tile, var):
    fname = '{var}_{tile}_sin_500m.tif'.format(var=var, tile=tile)
    return fname

def parameters():
    return ['tcwv', 'gtco3', 'aod550', 'sf']
