#!/bin/bash

mkdir -p 1718
mkdir -p 1617
mkdir -p 1516
mkdir -p 1415
mkdir -p 1314
mkdir -p 1213
mkdir -p 1112

wget http://www.football-data.co.uk/mmz4281/1718/data.zip 
unzip data.zip -d 1718
rm data.zip

wget http://www.football-data.co.uk/mmz4281/1617/data.zip
unzip data.zip -d 1617
rm data.zip

wget http://www.football-data.co.uk/mmz4281/1516/data.zip
unzip data.zip -d 1516
rm data.zip

wget http://www.football-data.co.uk/mmz4281/1415/data.zip
unzip data.zip -d 1415
rm data.zip

wget http://www.football-data.co.uk/mmz4281/1314/data.zip
unzip data.zip -d 1314
rm data.zip

wget http://www.football-data.co.uk/mmz4281/1213/data.zip
unzip data.zip -d 1213
rm data.zip

wget http://www.football-data.co.uk/mmz4281/1112/data.zip
unzip data.zip -d 1112
rm data.zip
