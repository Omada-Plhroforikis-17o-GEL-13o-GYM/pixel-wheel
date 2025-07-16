#!/bin/bash


cd src
rm -rf tleng2
git clone https://github.com/tl-ecosystem/tleng.git tleng-temp
mv tleng-temp/src/tleng2 tleng2
rm -rf tleng-temp
cd ..

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt