import datetime as dt
import calendar
import osr

import CAMS_utils
import cams


def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end + 1):
        y, m = divmod(ym, 12)
        yield y, m + 1


def latlon_from_sinu(easting, northing):
    """Converts from MODIS sinusoidal to lat/long coordinates"""
    wgs84 = osr.SpatialReference()
    modis_sinu = osr.SpatialReference()
    wgs84.ImportFromEPSG(4326)
    modis_sinu.ImportFromProj4(
        "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs")
    transform = osr.CoordinateTransformation(modis_sinu, wgs84)
    (lat, lon, z) = transform.TransformPoint(
        float(easting), float(northing), 0.0)
    return lat, lon


def get_extent(MOD09band):
    """
    Get min and maximum latitude and longitude from modis band.
    returns smallest and largest lat and long co-ordinates from tile.
    MODIS tile is in sinusoidal co-ords and not square in lat lon coordinates.
    This function selects the most eastward(westward) of the Upper and lower 
    right (left) corner coordinates. As MODIS tiles don't cross the equator 
    this should encompas the tile extent. a margin of 0.1 degrees is added to 
    ensure the tile extent is encompassed.
    """
    (xmin, xmax, xres, ymin, ymax, yres) = CAMS_utils.get_tile_extent(MOD09band)
    UL = latlon_from_sinu(xmin, ymax)
    LL = latlon_from_sinu(xmin, ymin)
    UR = latlon_from_sinu(xmax, ymax)
    LR = latlon_from_sinu(xmax, ymin)
    minlon = min(UL[0], LL[0]) - 0.1
    maxlon = max(UR[0], LR[0]) + 0.1
    minlat = LL[1] - 0.1
    maxlat = UL[1] + 0.1

    print UL, LL, UR, LR
    print minlat, maxlat, minlon, maxlon
    return [maxlat, maxlon, minlat, minlon]


def download_cams(start_date, end_date, tile, extent, reproject=False, timesteps = [9,12,15]):
    """
    Download ECMWF CAMS data between startdate and enddate inclusive.
    The data will cover a tile that can either be provided via the location
    parameter as the [N (top), E (right), S (bottom), W (left)] lat/lon 
    cordinates or it can be inferred from the extent of a tile as read from 
    a modis tile via the MOD09band parameter.

    Parameters
    ----------
    startdate : a datetime.date object 
        the first date of data to be downloaded
    enddate : a datetime.date object the last date of data to be downloaded
    extent : Either an example modis band OR the corner coordinates of the tile in lat/lon projection:
        An example modis band (e.g. 'HDF4_EOS:EOS_GRID:"MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1')
            OR
        [N (top), E (right), S (bottom), W (left)] elements of tile in lat/lon projection.

    If given, the MOD09band (e.g. 'HDF4_EOS:EOS_GRID:"MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1')
    will be used to extract the required lat-lon extent. Otherwise the lat-lon extent must be provided.
    """
    # get extents
    try:
        location = get_extent(extent)
    except RuntimeError:
        pass

    # set parameters

    # TODO better to use variable list in CAMS_utils - modify cams.py for this to work?
    var = ("GEMS total column ozone",
           "total aerosol optical depth at 550 nm",
           "total column water vapour",
           "snowfall")
    grid = 0.125
    steptype = "fc"
    time = [0]
    # initialise cams

    # TODO! this could be paralellised - this can be done in the mars request but not in python.
    for year, month in month_year_iter(start_date.month, start_date.year, end_date.month, end_date.year):
        print year, month
        day, ndays = calendar.monthrange(year, month)
        start = dt.datetime(year, month, 1)
        end = dt.datetime(year, month, ndays)
        filename = CAMS_utils.nc_filename(tile, year, month)
        cams_downloader = cams.Query(var=var, grid=grid, area=location,
                                     type=steptype, time=time,
                                     step=timesteps,
                                     start_date=start, end_date=end,
                                     dformat="netcdf",filename=filename,
                                     dataset="cams_nrealtime")
        # download
        cams_downloader.download()
        if reproject:
            reproject_cams(modisband, year, month, tile, directory)

    print 'done'


def main():
    start_date = dt.date(2015, 1, 1)
    end_date = dt.date(2015, 12, 31)
    # location = [40, -0.0109, 30, -13.0541]
    tile = 'h17v05'
    modisband = 'HDF4_EOS:EOS_GRID:"/media/Data/modis/h17v05/MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1'
    return download_cams(start_date, end_date, tile, modisband, reproject=True, timesteps=[0,3,6,9,12,15,18,21,24])


if __name__ == "__main__":
    main()
