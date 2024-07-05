#!/bin/bash 
set -e
set -x

git clone https://github.com/fml-ethz/dt4dds-challenges.git

ln -s dt4dds-challenges/bin/dt4dds-challenges ./dt4dds-challenges