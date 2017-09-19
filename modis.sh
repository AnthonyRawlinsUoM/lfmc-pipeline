#!/bin/sh

GREP_OPTIONS=''

cookiejar=$(mktemp cookies.XXXXXXXXXX)
netrc=$(mktemp netrc.XXXXXXXXXX)
chmod 0600 "$cookiejar" "$netrc"

function finish {
  rm -rf "$cookiejar" "$netrc"
  dot_netrc_tmp=$(mktemp ~/.netrc.tmp.XXXXXXXXXX)
  chmod 0600 "$dot_netrc_tmp"
  if [ -e ~/.netrc ]
  then
    awk '!/nrt3\.modaps\.eosdis\.nasa\.gov/' ~/.netrc > $dot_netrc_tmp && mv $dot_netrc_tmp ~/.netrc
  fi
}

trap finish EXIT
WGETRC="$wgetrc"

prompt_credentials() {
    echo "Enter your Earthdata Login or other provider supplied credentials"
    read -p "Username (anthonyrawlinsuom): " username
    username=${username:-anthonyrawlinsuom}
    read -s -p "Password: " password
    echo "\nmachine urs.earthdata.nasa.gov\tlogin $username\tpassword $password" >> $netrc
    echo "\nmachine nrt3.modaps.eosdis.nasa.gov\tlogin $username\tpassword $password" >> $netrc
    echo
}

exit_with_error() {
    echo
    echo "Unable to Retrieve Data"
    echo
    echo $1
    echo
    echo "ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/254/MOD09.A2017254.0020.006.NRT.hdf"
    echo
    exit 1
}

prompt_credentials

  detect_app_approval() {
    approved=`curl -s -b "$cookiejar" -c "$cookiejar" -L --max-redirs 2 --netrc-file "$netrc" ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/254/MOD09.A2017254.0020.006.NRT.hdf -w %{http_code} | tail  -1`
    if [ "$approved" -ne "302" ]; then
        # User didn't approve the app. Direct users to approve the app in URS
        exit_with_error "Please ensure that you have authorized the remote application by visiting the link below "
    fi
}

setup_auth_curl() {
    # Firstly, check if it require URS authentication
    status=$(curl -s -z "$(date)" -w %{http_code} ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/254/MOD09.A2017254.0020.006.NRT.hdf | tail -1)
    if [[ "$status" -ne "200" && "$status" -ne "304" ]]; then
        # FTP retrieval. Set netrc file before curl-ing.
        echo "\nmachine nrt3.modaps.eosdis.nasa.gov\tlogin $username\tpassword $password" >> $netrc
    fi
}

setup_auth_wget() {
    # The safest way to auth via curl is netrc. Note: there's no checking or feedback
    # if login is unsuccessful
    touch ~/.netrc
    chmod 0600 ~/.netrc
    ftp_hostname='nrt3.modaps.eosdis.nasa.gov'
    credentials=$(grep $ftp_hostname ~/.netrc)
    if [ -z "$credentials" ]; then
        echo "\nmachine nrt3.modaps.eosdis.nasa.gov\tlogin $username\tpassword $password" >> ~/.netrc
    fi
    credentials=$(grep 'machine urs.earthdata.nasa.gov' ~/.netrc)
    if [ -z "$credentials" ]; then
        cat "$netrc" >> ~/.netrc
    fi
}

    fetch_urls() {
    if command -v curl >/dev/null 2>&1; then
        setup_auth_curl
        while read -r line; do
            curl -f -Og --netrc-file "$netrc" $line && echo || exit_with_error "Command failed with error. Please retrieve the data manually."
        done;
    elif command -v wget >/dev/null 2>&1; then
        # We can't use wget to poke provider server to get info whether or not URS was integrated without download at least one of the files.
        echo
        echo "WARNING: Can't find curl, use wget instead."
        echo "WARNING: Script may not correctly identify Earthdata Login integrations."
        echo
        setup_auth_wget
        while read -r line; do
        wget --load-cookies "$cookiejar" --save-cookies "$cookiejar" --keep-session-cookies -- $line && echo || exit_with_error "Command failed with error. Please retrieve the data manually."
        done;
    else
        exit_with_error "Error: Could not find a command-line downloader.  Please install curl or wget"
    fi
}

fetch_urls <<'EDSCEOF'
  ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/254/MOD09.A2017254.0020.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/253/MOD09.A2017253.0115.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/252/MOD09.A2017252.2335.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/252/MOD09.A2017252.0030.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/251/MOD09.A2017251.0125.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/250/MOD09.A2017250.2350.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/250/MOD09.A2017250.2345.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/250/MOD09.A2017250.0045.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/250/MOD09.A2017250.0040.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/249/MOD09.A2017249.2305.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/249/MOD09.A2017249.0000.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/248/MOD09.A2017248.0055.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/247/MOD09.A2017247.2320.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/247/MOD09.A2017247.2315.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/247/MOD09.A2017247.0015.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/247/MOD09.A2017247.0010.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/246/MOD09.A2017246.0110.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/246/MOD09.A2017246.0105.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/245/MOD09.A2017245.2330.006.NRT.hdf
ftp://nrt3.modaps.eosdis.nasa.gov/allData/6/MOD09/2017/245/MOD09.A2017245.0025.006.NRT.hdf

EDSCEOF
