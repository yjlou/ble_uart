#!/usr/bin/env python3
"""A JSON RPC server.

https://pypi.org/project/json-rpc/
"""
from jsonrpc import JSONRPCResponseManager, dispatcher
from ptyprocess import PtyProcessUnicode
import shlex
import sys
import threading
import traceback
import time

sys.path.append('.')  # to import file in the current directory.

from ble_uart.utils import LOG
import process_unit
import utils


class JsonRpcServer(process_unit.ProcessUnit):
  def __init__(self, funcs:dict={}):
    """Constructor.

    Args:
      funcs: dict of callable where the key is the function name.
    """
    super().__init__()

    self._funcs = funcs
    self.flow(0).set_egress(self.rx)

  def rx(self, data:bytearray):

    try:
      data = bytes(data)
      data = data.decode('utf-8')

      # Copy all funcs to the dispatcher.
      for key, value in self._funcs.items():
        dispatcher[key] = value

      response = JSONRPCResponseManager.handle(data, dispatcher)
      self.flow(1).ingress(utils.str_to_bytearray(response.json))

    except EOFError as err:
      LOG.error(f'Detected EOF in exec.process_loop. Stop.')
    except Exception as err:
      LOG.error(f'Error in JsonRpcServer.rx(): {err}')
      traceback.print_stack()
    finally:
      self.terminate()

  def start(self, new_dev):
    LOG.info(f'Here comes a new device: {new_dev}')

  def terminate(self):
    LOG.info(f'Terminating the pipe ...')

  def stop(self):
    LOG.info(f'The device is disconnected.')
