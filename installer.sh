#!/bin/bash
echo "It is necessary: node.js, python3 and pip to continue"

echo "Getting python-node connection"
pip install nodejs-bin

echo "Installing feedreader dependencies"
cd feedreader
pip install feedparser 
pip install python-dateutil --upgrade
cd ../

echo "Installing webscrapping dependencies"
cd scraping
npm install

echo "Run the python script Main.py to test"