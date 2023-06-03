#!/bin/bash

# get version from plugin.yaml but only the first instance, remove \""
version=$(grep -m1 version ../plugin.yaml | cut -d '"' -f 2)

# build release
mkdir tacticalrmm-$version
cp -r ../contents tacticalrmm-$version/
cp -r ../resources tacticalrmm-$version/
cp ../plugin.yaml tacticalrmm-$version/

# create zip & send to rundeck
zip -r tacticalrmm-$version.zip tacticalrmm-$version

if [ "$1" == "test" ]; then
    docker cp tacticalrmm-$version.zip rundeck:/home/rundeck/libext/tacticalrmm-$version.zip
    rm tacticalrmm-$version.zip
fi

# cleanup
rm -rf tacticalrmm-$version