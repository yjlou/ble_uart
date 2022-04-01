#!/usr/bin/env bash
#
#  Please run me at least once to get the necesssary files.
#
#  Run this script on both host and target devices.
#

set -e

# Download simple JSON RPC Javascript.
echo
echo '- Install packages ...'
echo
sudo apt install -y wget openssl python3 bluez netcat
pip3 install -r requirements.txt

# Download simple JSON RPC Javascript.
echo
echo "- Download the simple-jsonrpc-js.js ..."
echo
wget https://raw.githubusercontent.com/jershell/simple-jsonrpc-js/master/simple-jsonrpc-js.js \
    -O js/simple-jsonrpc-js.js

# Download the simple HTTP server
echo
echo '- Download the simple HTTP server ...'
echo
wget https://gist.githubusercontent.com/dergachev/7028596/raw/abb8bd2b53501ff7125b93e8d975e77ffd756bf1/simple-https-server.py

# Generate server.pem
echo
echo
echo '--------------------------------------------------------------------'
echo '-                                                                  -'
echo '- Generate server.pem file for development (optional) ...          -'
echo '-                                                                  -'
echo '- You will be prompted to enter the address info for certificate.  -'
echo '- Feel free to enter empty info.                                   -'
echo '-                                                                  -'
echo '--------------------------------------------------------------------'
echo
echo
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

echo
echo '- Done'
echo
