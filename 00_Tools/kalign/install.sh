#!/bin/bash 
cd "$(dirname "$0")"
set -e
set -x

wget https://github.com/TimoLassmann/kalign/archive/refs/tags/v3.4.0.tar.gz
tar -zxvf v3.4.0.tar.gz -C .
rm v3.4.0.tar.gz
mkdir build
cd build
cmake ../kalign-3.4.0
make 
cd ..
cp build/src/kalign ./kalign