#!/usr/bin/env python3
"""Read/write from/into files (or file-like, for example, named pipe).
"""
import sys
import time
import threading

sys.path.append('.')  # to import file in the current directory.

from ble_uart.utils import LOG
import process_unit
import utils


class FileIo(process_unit.ProcessUnit):
  def __init__(self, read_filename, write_filename):
    super().__init__()
    self._read_filename = read_filename
    self._read_fp = None
    self._write_filename = write_filename
    self._write_fp = None
    self._processing = False
    self.flow(0).set_egress(self.rx)

  def rx(self, data:bytearray):
    if self._write_fp:
      try:
        self._write_fp.write(bytes(data).decode('utf-8'))
      except Exception as err:
        LOG.error(f'Error while sending to the file: {err}')

  def start(self, new_dev):
    LOG.info(f'Here comes a new device: {new_dev}')
    self._write_fp = open(self._write_filename, 'w')
    threading.Thread(target=self.process_loop).start()

  def process_loop(self):
    if self._processing:
      return

    try:
      self._processing = True
      time.sleep(3)  # Give 3 secs for BLE to update the norify=False so that we can queue
                     # the very first N bytes in Nus._buf.
      self._read_fp = open(self._read_filename, 'r')

      while True:
        data = self._read_fp.read(1)
        if not data:
          raise EOFError
        self.flow(1).ingress(utils.str_to_bytearray(data))

    except EOFError as err:
      LOG.error(f'Detected EOF in file_io.process_loop. Stop.')
    finally:
      self._read_fp.close()
      self._read_fp = None
      self._processing = False

  def stop(self):
    if self._write_fp:
      self._write_fp.close()
      self._write_fp = None

    LOG.info(f'The device is disconnected.')
