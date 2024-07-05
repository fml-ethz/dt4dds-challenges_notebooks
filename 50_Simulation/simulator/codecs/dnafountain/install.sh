#!/bin/bash 
set -e

git clone https://github.com/jdbrody/dna-fountain.git
python3 -m virtualenv venv
source venv/bin/activate
pip3 install setuptools numpy cython Cython tqdm scipy Biopython reedsolo
cd dna-fountain
python setup.py build_ext --inplace
pip install .
