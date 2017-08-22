import gdal
import subprocess
import CAMS_utils
import datetime as dt

gdal.UseExceptions()


def get_tile_extent(MOD09band):
    return CAMS_utils.get_tile_extent(MOD09band)


def reproject(var, infname, outfname, xmin, xmax, ymin, ymax):
    args = ['./reprojectCAMS.sh', '-i', infname, 
            '-o', outfname, 
            '-p', var, 
            '--xmin', str(xmin), 
            '--ymin', str(ymin), 
            '--xmax', str(xmax), 
            '--ymax', str(ymax)]
    print args
    subprocess.call(args)


def reproject_cams(MOD09band, year, month, tile, directory):
    #Get extent and resolution of modis file
    xmin, xmax, xres, ymin, ymax, yres = get_tile_extent(MOD09band)
    # Loop through variables
    vars =  CAMS_utils.parameters()
    for var in vars:
        #Get input file 
        infname = CAMS_utils.nc_filename(tile, year, month,
                                 directory=directory, checkpath = False)
        #create output filename
        print directory
        outfname = CAMS_utils.vrt_filename(tile, year, month, var,
                                   directory=directory)
        #reproject image
        reproject(var, infname, outfname, xmin, xmax, ymin, ymax)


def main():
    modisband = 'HDF4_EOS:EOS_GRID:"/media/Data/modis/h17v05/MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1'
    year = 2016
    month = 1
    tile = 'h17v05'
    directory = "data"
    reproject_cams(modisband, year, month, tile, directory)

if __name__ == "__main__":
    main()
