#!/usr/bin/env python3
"""The Echo Server.

Reply whatever receiving from the BLE.
"""
import sys

sys.path.append('.')  # to import file in the current directory.

from ble_uart.utils import LOG
from nus import Nus
import process_unit
from pipeline import Pipeline

class Echo(process_unit.ProcessUnit):
  def __init__(self):
    super().__init__()
    self.flow(0).set_egress(self.rx)

  def rx(self, data:bytearray):
    LOG.info(f'RX: {data} --> TX')
    self.flow(1).ingress(data)

  def start(self, new_dev):
    LOG.info(f'CONNECTED: {new_dev}')

  def stop(self):
    LOG.info(f'DISCONNECTED:')
