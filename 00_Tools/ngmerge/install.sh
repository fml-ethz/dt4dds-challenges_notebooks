#!/bin/bash 
cd "$(dirname "$0")"
set -e
set -x

wget https://github.com/jsh58/NGmerge/archive/refs/tags/v0.3.tar.gz
tar -zxvf v0.3.tar.gz -C .
rm v0.3.tar.gz
cd NGmerge-0.3
make
cd ..
cp NGmerge-0.3/NGmerge ./ngmerge
