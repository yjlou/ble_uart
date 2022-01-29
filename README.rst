===============
BLE UART Daemon
===============

This program runs on the Raspberry Pi and creates a BLE Nordic UART Service (NUS_) for phone or
HTML5 webpage to connect.

.. _NUS: https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.sdk5.v14.0.0%2Fble_sdk_app_nus_eval.html

This is useful for Raspberry Pi developer/user to connect the board without an IP network.
Just download an off-the-shelf BLE UART app (listed below_). Then you are ready to connect.

.. image:: docs/login.gif
  :width: 400
  :alt: Login example

Install Packages
----------------

.. code-block:: bash
  sudo apt install bluez netcat
  pip3 install -r requirements.txt

Running the Program
-------------------

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

.. _below:

Verified Apps on Android
------------------------

* Serial Bluetooth Terminal (recommended)
* My-nRF52-toolbox
* nRF Toolbox


Verified Apps on iOS
--------------------

Verified Web Browsers
---------------------
