===============
BLE UART Daemon
===============

This program runs on the Raspberry Pi and creates a Nordic UART Service (NUS_).

.. NUS_: https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.sdk5.v14.0.0%2Fble_sdk_app_nus_eval.html

for phone or HTML5 webpage to connect.

.. image:: docs/login.gif
  :width: 400
  :alt: Login example


Running the Program
-------------------

sudo apt install bluez netcat
pip3 install -r requirements.txt

.. code-block:: bash

  # By default, use STDIN/STDOUT as the input/output.
  ./ble_uart.py --name MyBleUart

  # Start as an echo server. Whatever sent from the App will return to the App.
  ./ble_uart.py -e

  # Provide a login shell.
  ./ble_uart.py -l

  # Launch a command after BLE connection is established.
  ./ble_uart.py -c "netcat google.com 80"


Verified Platforms
------------------

* Raspberry Pi Zero 1/2 W


Verified Apps on Android
------------------------

* Serial Bluetooth Terminal (recommended)
* My-nRF52-toolbox
* nRF Toolbox

Verified Apps on iOS
--------------------

Verified Web Browsers
---------------------
