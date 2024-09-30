#!/bin/bash 
cd "$(dirname "$0")"
set -e
set -x

wget https://sourceforge.net/projects/bbmap/files/BBMap_39.01.tar.gz/download
tar -zxvf download -C .
mv bbmap/* .
rm download
rmdir bbmap