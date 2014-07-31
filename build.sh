#!/bin/bash

VOLTDIST="voltdb"
PATH=`pwd`/$VOLTDIST/bin:$PATH
example_dir=$VOLTDIST/examples
download_path="http://github.com/VoltDB/app-%s/archive/master.tar.gz"

function help() {
    echo "Usage: ./build.sh path-to-voltdb-download.tar.gz"
}

if [ $# -ne 1 ]; then help; exit; fi

# download volt and unpacks it to voltdb/ first
rm -rf $VOLTDIST
mkdir $VOLTDIST
curl -sL $1 | tar xzC $VOLTDIST --strip-components 1

# download all apps and compile them, apps are listed in apps.txt
while read i; do
    outdir=$example_dir/$i
    # if the app is already there, skip the download
    if [ ! -d $outdir ]; then
        mkdir $outdir
        curl -sL `printf $download_path $i` | tar xzC $outdir --strip-components 1
    fi
    pushd $outdir
    ./run.sh demo-compile
    if [ $? != 0 ]; then exit; fi
    popd
done < apps.txt

# build the docker image
docker build --force-rm=true -t nshi/voltdb .
