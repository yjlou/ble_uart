#!/usr/bin/env python3
"""Execute a program.
"""
import shlex
from ptyprocess import PtyProcessUnicode
import sys
import threading
import time

sys.path.append('.')  # to import file in the current directory.

from ble_uart.utils import LOG
import process_unit
import utils


class Exec(process_unit.ProcessUnit):
  def __init__(self, program):
    super().__init__()
    self._program = program
    self._pipe = None
    self.flow(0).set_egress(self.rx)

  def rx(self, data:bytearray):
    if self._pipe:
      try:
        self._pipe.write(bytes(data).decode('utf-8'))
      except Exception as err:
        LOG.error(f'Error while sending to the program: {err}')

  def start(self, new_dev):
    LOG.info(f'Here comes a new device: {new_dev}')
    self._pipe = PtyProcessUnicode.spawn(shlex.split(self._program))
    threading.Thread(target=self.process_loop).start()

  def process_loop(self):
    time.sleep(3)  # Give 3 secs for BLE to update the norify=False so that we can queue
                   # the very first N bytes in Nus._buf.
    try:
      while True:
        data = self._pipe.read(20)
        if not data:
          raise EOFError
        self.flow(1).ingress(utils.str_to_bytearray(data))

    except EOFError as err:
      LOG.error(f'Detected EOF in exec.process_loop. Stop.')
    finally:
      self.terminate()

  def terminate(self):
    LOG.info(f'Terminating the pipe ...')
    self._pipe.terminate(force=True)
    self._pipe = None

  def stop(self):
    if self._pipe:
      LOG.info(f'The device is disconnecting...')
      self.terminate()
    LOG.info(f'The device is disconnected.')
