#!/usr/bin/env python3
"""The BLE controller.

This class accepts a 'services' structure which describes the BLE services and their
callback functions for read/write.

"""
import traceback

from ble_uart.utils import LOG
from bluezero import adapter
from bluezero import peripheral

import utils

# Characteristic User Descriptions
UUID_CUD = '2901'


def callback(func):
  """Used for BLE callback to dump error.

  @ble_controller.callback
  def ssid_char_write(self):
    ...

  Args:
    func: the function object to call.

  Returns:
    whatever 'func' returns.
  """
  def call(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except:
      LOG.error(f'callback ERROR: {func}({args}, {kwargs})')
      traceback.print_stack()
      traceback.print_exc()
      raise
  return call


class BleController(object):

  def __init__(self,
               services:dict,
               local_name:str=None,
               adapter_address:str=None,
               on_connect=None,
               on_disconnect=None,
               encryption=False):
    """Constructor.

    Args:
      services: dict. See the exaple in the main() below.
      local_name: str. optional. Human-readable string shown in the scan result.
      adapter_address: colon-split string. optional.
    """
    # If adapter_address is not provided, use the first interface we found.
    self._adapter_address = (adapter_address if adapter_address
                             else list(adapter.Adapter.available())[0].address)
    # If the local name is not provided, use the default prefix plus the last 2 bytes inthe adapter
    # address.
    self._local_name = (local_name if local_name
                        else 'Datopia_{}'.format(''.join(self._adapter_address.split(':')[-2:])))
    self._services = services
    self._on_connect = on_connect
    self._on_disconnect = on_disconnect
    self._encryption = encryption

  @property
  def local_name(self):
    return self._local_name

  @property
  def adapter_address(self):
    return self._adapter_address

  def start(self):
    """Start the BLE service. Never return."""
    self._peripheral = peripheral.Peripheral(self._adapter_address,
                                             local_name=self._local_name,
                                             appearance=1344)

    primary = True  # Only True for the first service.
    srv_id = 0
    for serv_name, service in self._services.items():
      self._peripheral.add_service(srv_id=srv_id, uuid=service['uuid'], primary=primary)
      primary = False

      chr_id = 0
      for char_name, char in service['characteristics'].items():
        reads = ['encrypt-read'] if self._encryption else ['read']
        writes = ['encrypt-write'] if self._encryption else ['write']
        notifys = ['notify'] if char.get('notify') else []
        char_flags = (reads +  # so that CUD can be read.
                      notifys +
                      (writes if 'write' in char else []))

        self._peripheral.add_characteristic(
            srv_id=srv_id, chr_id=chr_id,
            uuid=char['uuid'],
            value=[],
            notifying=False,
            flags=char_flags,
            read_callback=callback(char.get('read')),
            write_callback=callback(char.get('write')),
            notify_callback=callback(char.get('notify'))
        )
        self._peripheral.add_descriptor(
            srv_id=srv_id, chr_id=chr_id, dsc_id=0, uuid=UUID_CUD,
            value=utils.str_to_list(char_name), flags=['read']
        )

        chr_id += 1

      srv_id += 1

    self._peripheral.on_connect = self._on_connect
    self._peripheral.on_disconnect = self._on_disconnect
    self._peripheral.publish()  # never return

  def stop(self):
    pass  # TODO: find a way to stop the BLE service.
