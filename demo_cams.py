import datetime as dt
from download_cams import download_cams
from read_cams import read_cams

# Download and reproject

# The code will download complete months even if the start/end date is
# part way through a month.
start_date = dt.date(2017, 1, 1)
end_date = dt.date(2017, 8, 31)
tile = 'h17v05'  # This is just used to label the files
directory = 'data'  # Location to store the data
# Example modis file. The required extent will be extracted from this:
modis_file = "/media/Data/modis/h17v05/MOD09GA.A2016009.h17v05.006.2016012053256.hdf"
master = 'HDF4_EOS:EOS_GRID:{}:MODIS_Grid_500m_2D:sur_refl_b02_1'.format(modis_file)
# Alternatively the required extent can be passed in as lat/lon co-ordinates
# e.g. master = [40, -0.0109, 30, -13.0541] (only if reproject = False)
timesteps = [9, 12, 15]  # (Optional) Time steps (in UTC) to download

download_cams(start_date, end_date, tile, master, directory, reproject=True,  timesteps=timesteps)


# Read in
datetime = dt.datetime(2016, 2, 15, 10, 0, 0)
data, uncertaint, times = read_cams(datetime, tile, directory)
