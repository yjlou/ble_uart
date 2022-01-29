#!/usr/bin/env python3
"""The NUS (Nordic UART Service).

Checkout the document on the following pages:

* https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/uart-service
* https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.sdk5.v14.0.0%2Fble_sdk_app_nus_eval.html
* https://bluezero.readthedocs.io/en/stable/examples.html#peripheral-nordic-uart-service
"""
import threading

import ble_controller
import process_unit


def getNusService(ble_rx:callable=None,
                  ble_tx:callable=None,
                  notify:callable=None):
  """Helper function to generate a dict for the BLE service.

  Args:
    ble_rx: callable(data:bytearray). Called when receiving date from peer device.
    ble_tx: callable():bytearray. Called when the peer device asks for data. This callback should
                                  return data to return.
    notify: callable(notifying:bool, characteristic:bluezero.localGATT.Characteristic). Called when
                              the notification state is changed by the peer. The |charateristic| can
                              be saved for future update.
  """
  return {
      'uuid': '6E400001-B5A3-F393-E0A9-E50E24DCCA9E',
      'characteristics': {
          'RX': {  # from other to me
              'uuid': '6E400002-B5A3-F393-E0A9-E50E24DCCA9E',
              'write': lambda data, option: ble_rx(data),
          },
          'TX': {  # from me to other
              'uuid': '6E400003-B5A3-F393-E0A9-E50E24DCCA9E',
              'read': ble_tx,
              'notify': notify,
          },
      },
  }


class Nus(process_unit.ProcessUnit):

  def __init__(self,
               local_name:str=None,
               on_connect:callable=None,
               on_disconnect:callable=None):
    super().__init__()

    self._local_name = local_name
    self._on_connect = on_connect
    self._on_disconnect = on_disconnect
    self._update_characteristic = None
    self._ble_ctl = None
    self._ble_thread = None
    self._buf = bytearray()
    self._started = False

    self.flow(1).set_egress(self.update_value)

  @property
  def ble_ctl(self):
    return self._ble_ctl

  @ble_controller.callback
  def update_value(self, data: bytearray):
    # TODO: handle > 20 bytes?
    if self._update_characteristic:
      self._update_characteristic.set_value(data)
    else:
      self._buf += data

  @ble_controller.callback
  def notify_callback(self, notifying, characteristic):
    print(f'NOTIFY: {notifying} / {characteristic}')
    if notifying:
      self._update_characteristic = characteristic
      if self._buf:
        self._update_characteristic.set_value(self._buf)
        self._buf = bytearray()
    else:
      self._update_characteristic = None

  def ble_tx(self, data: bytearray):
    self.update_value(data)

  def start(self):
    if self._started:
      reutnr

    self._ble_ctl = ble_controller.BleController(
        local_name=self._local_name,
        services={
            'UART': getNusService(
                ble_rx=self.flow(0).ingress,
                ble_tx=None,  # TODO: read from buffer.
                notify=lambda notifying, characteristic: self.notify_callback(notifying, characteristic)),
        },
        on_connect=self._on_connect,
        on_disconnect=self._on_disconnect
    )
    self._ble_thread = threading.Thread(target=self._ble_ctl.start)
    self._ble_thread.start()
    self._started = True

  def stop(self):
    pass  # TODO: kill the thread.
