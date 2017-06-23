#!/bin/bash 

while [[ $# -gt 1 ]]
do
key="$1"

case $key in 
    -i|--input)
    INPUTFILE="$2"
    shift
    ;;
    -o|--output)
    OUTPUTFILE="$2"
    shift
    ;;
    -p|--parameter)
    PARAMETER="$2"
    shift
    ;;
    --xmin)
    XMIN="$2"
    shift
    ;;
    --xmax)
    XMAX="$2"
    shift
    ;;
    --ymin)
    YMIN="$2"
    shift
    ;;
    --ymax)
    YMAX="$2"
    shift
    ;;
    *)
         #unknown option
    ;;
esac
shift
done
# "atmosvar_fc.nc":sf sf_h17v03_sin_500m.tif
#xmin=-1111950.52
#ymin=3335851.559
#xmax=0.0
#ymax=4447802.079
#XMIN = -13.0541
#YMIN = 30
#XMAX = 0.0109
#YMAX = 40

gdalwarp \
    -s_srs EPSG:4326 \
    -t_srs '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs ' \
    -te $XMIN $YMIN $XMAX $YMAX \
    -te_srs EPSG:4326 \
    -tr 463.312719959778804 -463.312716551443543 \
    -co "COMPRESS=LZW" -co "INTERLEAVE=BAND" -co "TILED=YES" \
    NETCDF:"$INPUTFILE":$PARAMETER $OUTPUTFILE
