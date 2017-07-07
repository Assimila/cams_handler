import gdal
import subprocess
import CAMS_utils

gdal.UseExceptions()

def input_filename(tile):
    return  CAMS_utils.nc_filename(tile)

def output_filename(tile, var):
    return CAMS_utils.reproj_geotiff_filename(tile, var)

def get_tile_extent(MOD09band):
    return  CAMS_utils.get_tile_extent(MOD09band)

def reproject(var, infname, outfname, xmin, xmax, xres, ymin, ymax, yres):
    args = ['./reprojectCAMS.sh', '-i', infname, 
            '-o', outfname, 
            '-p', var, 
            '--xmin', str(xmin), 
            '--ymin', str(ymin), 
            '--xmax', str(xmax), 
            '--ymax', str(ymax)]
    print args
    subprocess.call(args)

def reproject_cams(MOD09band, tile = 'h17v05'):
    #Get extent and resolution of modis file
    xmin, xmax, xres, ymin, ymax, yres = get_tile_extent(MOD09band)
    # Loop through variables
    vars =  CAMS_utils.parameters()
    for var in vars:
        #Get input file 
        infname = input_filename(tile)
        #create output filename
        outfname = output_filename(tile, var)
        #reproject image
        reproject(var, infname, outfname, xmin, xmax, xres, ymin, ymax, yres)
        print xmin, xmax, xres, ymin, ymax, yres, infname, outfname
        


def main():
    modisband = 'HDF4_EOS:EOS_GRID:"/media/Data/modis/h17v05/MOD09GA.A2016009.h17v05.006.2016012053256.hdf":MODIS_Grid_500m_2D:sur_refl_b02_1'
    reproject_cams(modisband)

if __name__ == "__main__":
    main()
