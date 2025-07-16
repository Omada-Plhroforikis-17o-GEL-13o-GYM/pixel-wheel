#!/bin/bash
git pull origin main
rm -rf src/tleng2

cd src
rm -rf tleng2
git clone https://github.com/tl-ecosystem/tleng.git tleng-temp
mv tleng-temp/src/tleng2 tleng2
rm -rf tleng-temp
cd ..

python setup.py build