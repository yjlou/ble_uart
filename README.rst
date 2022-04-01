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

Verified Platforms
------------------

* Raspberry Pi Zero 1/2 W

Install Packages
----------------

.. code-block:: bash

  ./envsetup.sh

Running the Program
-------------------

This program supports the following modes:

.. code-block:: bash

  # By default, use STDIN/STDOUT as the input/output.
  ./ble_uart.py --name MyBleUart

  # Start as an echo server. Whatever sent from the App will return to the App.
  ./ble_uart.py -e

  # Provide a login shell.
  ./ble_uart.py -l

  # Launch a command after BLE connection is established.
  ./ble_uart.py -c "netcat google.com 80"

  # Run as a JSON RPC server
  examples/json_rpc/json_rpc.py
  # Check the message to get the URL for the RPC client.

Once the program is launched, it will advertise a BLE UART service. Use the following BLE apps or
browsers to search a device named 'BLE_UART' and then connect it to use.

.. _below:

Verified Apps on Android
------------------------

* Serial Bluetooth Terminal (recommended)
* My-nRF52-toolbox
* nRF Toolbox


Verified Apps on iOS
--------------------

Under construction.


Verified Web Browsers
---------------------

Click the following web_page_ link to connect the Raspberry Pi through the browser.

.. _web_page: https://raw.githack.com/yjlou/ble_uart/master/examples/ble_uart/ble_uart.html

* Chrome

For full list, check the browser implementation_ status.

.. _implementation: https://github.com/WebBluetoothCG/web-bluetooth/blob/main/implementation-status.md


How to run the HTML/javascript examples in local
------------------------------------------------

.. code-block:: bash
  # At root path. Make sure you have run ./envsetup.sh once to get the cert files.
  python simple-https-server.py

  # Visit https://localhost/examples/ble_uart/ble_uart.html
  # Or    https://localhost/examples/json_rpc/json_rpc.html


Troubleshooting the BLE
-----------------------

.. code-block:: bash

  # On Raspberry Pi board.

  # stop the ble_uart.py

  utils/restart_bluetooth.sh

  # restart the ble_uart.py
