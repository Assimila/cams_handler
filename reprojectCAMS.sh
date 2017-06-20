#!/bin/bash

xmin=-1111950.52
ymin=3335851.559
xmax=0.0
ymax=4447802.079

gdalwarp \
    -s_srs EPSG:4326 \
    -t_srs '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs ' \
    -te $xmin $ymin $xmax $ymax \
    -tr 463.312719959778804 -463.312716551443543 \
    -co "COMPRESS=LZW" -co "INTERLEAVE=BAND" -co "TILED=YES" \
    NETCDF:"atmosvar_fc.nc":tcwv tcwv_h17v03_sin_500m.tif
