download_cams.py: Download cams data. Can also reproject onto MODIS grid

reproject_cams.py: Reproject downloaded CAMS data onto MODIS sinusoidal grid

read_cams.py: Read in reprojected CAMS data (in VRT format) and return data and uncertainty.

demo_cams.py: Demonstration of how to run.

Dependancies:
Requires gdal with netcdf support.

IMPORTANT: in order to run download_cams you will need to install ecmwfapi
e.g.    conda install -c conda-forge ecmwf-api-client
 You also need to register for ECMWF and obtain an ECMWF API key.
https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+Datasets
This isn't necessary if you just want to read in the already downloaded data.
