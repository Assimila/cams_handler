import datetime as dt
import calendar
import osr

import CAMS_utils
from reproject_cams import reproject_cams
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
    """ Get min and maximum latitude and longitude from modis band.
    Returns smallest and largest lat and long co-ordinates from tile. MODIS tile is in sinusoidal co-ordinates and not
    square in lat lon coordinates. This function selects the most eastward(westward) of the Upper and lower right (left)
    corner coordinates. As MODIS tiles don't cross the equator this should encompass the tile extent. a margin of 0.1
    degrees is added to ensure the tile extent is encompassed.
    Input:
        MOD09band : (string) modis band in format e.g.
        'HDF4_EOS:EOS_GRID:"MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1'
    """
    (xmin, xmax, xres, ymin, ymax, yres) = CAMS_utils.get_tile_extent(MOD09band)
    ul = latlon_from_sinu(xmin, ymax)
    ll = latlon_from_sinu(xmin, ymin)
    ur = latlon_from_sinu(xmax, ymax)
    lr = latlon_from_sinu(xmax, ymin)
    minlon = min(ul[0], ll[0]) - 0.1
    maxlon = max(ur[0], lr[0]) + 0.1
    minlat = ll[1] - 0.1
    maxlat = ul[1] + 0.1
    return [maxlat, maxlon, minlat, minlon]


def download_cams(start_date, end_date, tile, extent, directory, reproject=False, timesteps=(9, 12, 15)):
    """ Download ECMWF CAMS data between startdate and enddate inclusive.
    The data will cover a tile that can either be provided via the location parameter as the
    [N (top), E (right), S (bottom), W (left)] lat/lon cordinates or it can be inferred from the extent of a tile as
    read from a modis tile via the MOD09band parameter.

    Inputs:
        start_date : a datetime.date object. The first date of data to be downloaded.
        end_date : a datetime.date object the last date of data to be downloaded
        tile : (string) reference to MODIS tile, e.g. h17v05. Only used in file names.
        extent : Either an example MODIS band OR the corner coordinates of the tile in lat/lon projection:
                An example MODIS band (e.g.
                'HDF4_EOS:EOS_GRID:"MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1')
                    OR
                [N (top), E (right), S (bottom), W (left)] elements of tile in lat/lon projection.
        directory : (string) location to store data
        reproject : (=False) (bool) if reproject == True a VRT file will be created that includes the reprojection
                    on to the MODIS grid. The extent variable must be a MODIS band if reproject == True.
        timesteps : (=(9, 12, 15)) the forcast timesteps in UTC. Available steps are every 3 hours from 0 to 21.
                    Default steps are chosen to be near sentinel overpass times.
    """
    # Get extents
    try:
        location = get_extent(extent)
    except RuntimeError as e:
        if isinstance(extent, str):
            raise('cannot open {}'.format(extent), e)
        location = extent

    # Set parameters
    var = CAMS_utils.parameters()
    grid = 0.125
    steptype = "fc"
    time = [0]

    # TODO! this could be paralellised. (This can be done in the mars request on the command line but not in python.)
    for year, month in month_year_iter(start_date.month, start_date.year, end_date.month, end_date.year):
        print year, month
        day, ndays = calendar.monthrange(year, month)
        start = dt.datetime(year, month, 1)
        end = dt.datetime(year, month, ndays)
        # Initialise cams
        filename = CAMS_utils.nc_filename(tile, year, month, directory)
        cams_downloader = cams.Query(var=var, grid=grid, area=location,
                                     mtype=steptype, time=time,
                                     step=timesteps,
                                     start_date=start, end_date=end,
                                     dformat="netcdf", filename=filename,
                                     dataset="cams_nrealtime")
        # Download
        cams_downloader.download()
        if reproject:
            reproject_cams(extent, year, month, tile, directory)
    print 'done'


def main():
    start_date = dt.date(2016, 1, 1)
    end_date = dt.date(2016, 12, 31)
    tile = 'h17v05'
    directory = 'data'
    modisband = 'HDF4_EOS:EOS_GRID:"/media/Data/modis/h17v05/MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1'
    # extent = [40, -0.0109, 30, -13.0541]  #Could be passed instead of modis band (only if reproject=False)
    timesteps = [9, 12, 15]
    return download_cams(start_date, end_date, tile, modisband, directory, reproject=True, timesteps=timesteps)


if __name__ == "__main__":
    main()
