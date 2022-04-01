#!/usr/bin/env bash
#
#  Sometimes the Bluetooth stack gets mad and the Chrome cannot connect to it for no reason.
#  It means it is the time to restart the bluetooth service.
#
#  Run this script on the target device.
#

set -e

echo '- Stopping Bluetooth service ...'
service bluetooth stop

echo '- Clean caches ...'
rm -rf  /var/lib/bluetooth/

echo '- Starting Bluetooth service ...'
service bluetooth start
