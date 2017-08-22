import datetime as dt
from download_cams import download_cams
from read_cams import read_cams

#Download and reproject

# The code will download complete months even if the start/end date is
#part way through a month.
start_date = dt.date(2017, 1, 1)
end_date = dt.date(2017, 8, 31)
tile = 'h17v05'  #This is just used to label the files
# Example modis file. The required extent will be extracted from this:
modis_file = "/media/Data/modis/h17v05/MOD09GA.A2016009.h17v05.006.2016012053256.hdf"
master = 'HDF4_EOS:EOS_GRID:{}:MODIS_Grid_500m_2D:sur_refl_b02_1'.format(modis_file)
#Althernatively the required extent can be passed in as lat/lon co-ordinates


download_cams(start_date, end_date, tile, MOD09band=master, reproject = True)


#read in
datetime = dt.datetime(2016, 2, 15, 10, 0, 0)
data, times = read_cams(datetime, tile, directory)