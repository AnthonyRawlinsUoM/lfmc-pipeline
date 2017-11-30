#!/bin/bash

product="MOD09A1"
version=5
lat=44.3
lon=99.7
date="2015-01-01,2015-03-31"

# Use inventory service to select files
for URL in `curl https://lpdaacsvc.cr.usgs.gov/services/inventory?product=$product\&version=$version\
&lat=$lat\&lon=$lon\&date=$date\&output=text 2> /dev/null`
do
        # Cut granules file name from URL, it's the last item in the URL
        FILE=`echo $URL | rev | cut -d\/ -f 1 | rev `
        echo "Getting file $FILE "
        # retrieve the file from data pool
        # curl $URL --output $FILE 2>/dev/null # old style call
        curl -n -L -c ~/.cookies -b ~/.cookies $URL --output $FILE 2>/dev/null  #new style call
done

