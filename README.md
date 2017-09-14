download_cams.py: Download cams data. Can also reproject onto MODIS grid

(reproject_cams.py: Reproject downloaded CAMS data onto MODIS sinusoidal grid)

read_cams.py: Read in reprojected CAMS data (in VRT format) and return data and uncertainty.

demo_cams.py: Demonstration of how to run.

read_cams finds the time-step closest to the time you input and returns the data at that time-step along with uncertainty (currently fixed at 10%)  and the time-stamp that matches the data.

Dependancies:
Requires gdal with netcdf support.

IMPORTANT: in order to run download_cams you will need to install ecmwfapi
e.g.    conda install -c conda-forge ecmwf-api-client
 You also need to register for ECMWF and obtain an ECMWF API key.
https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+Datasets
This isn't necessary if you just want to read in the already downloaded data.




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


    def read_cams(date, tile, directory, variables=None):
    """
    Input:
        date : a datetime object with year, month, day, hours, minutes, seconds
        tile : modis tile reference eg h17v05
    Output:
        data: a dictionary of var:data pairs. Data is a 2D array.
        unc: a dictionary of var:unc paris. Uncertainty is the uncertainty in data.
        times : a dictionary of var:time pairs. time is a datetime object with the date and time of the
               returned data.
        directory : (string) location of data
        variables : (=None) Parameters to read in e.g. [tcwv, 'gtco3', 'aod550', 'sf'].
                    If not specified the default list will be read from cams_utils.
    """