#!/usr/bin/env python3
"""This is an example code to show how to write a JSON RPC server.

Feel free to duplicate this file and customize your 'RPCs' dict.
"""
import argparse
import os
import sys
import threading
import time

sys.path.append(os.path.realpath('./'))  # to import file in the current directory.
sys.path.append(os.path.realpath('./ble_uart'))  # to import file in the ble_uart directory.

import ble_uart.json_rpc_server
from ble_uart.nus import Nus
import ble_uart.utils
from ble_uart.pipeline import Pipeline
from ble_uart.utils import LOG


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-n', '--name', dest='name', type=str, default=None,
                      help='The BLE device name')
PARSER.add_argument('--dry_run', dest='dry_run', action='store_true', default=False,
                    help='Dry run. Don\'t do nothing.')


def main():
  args = PARSER.parse_args()
  ble_uart.utils.die_when_dry_run(args)

  local_name = args.name if args.name else 'BLE_UART'
  late_bind = ble_uart.utils.LateBind()
  nus = Nus(local_name=local_name,
            on_connect=late_bind.start,
            on_disconnect=late_bind.stop)

  while True:
    try:
      RPCs = {
        'echo': lambda s: s,
        'add': lambda a, b: int(a) + int(b),
        'concat': lambda a, b, c: [a, b, c],
      }

      run_as = f'Run JSON RPC server'
      jserv = ble_uart.json_rpc_server.JsonRpcServer(RPCs)
      late_bind.set(jserv.start, jserv.stop)
      pipeline = Pipeline([nus, jserv])

      pipeline.compose()
      nus.start()

      LOG.info(f'Created BLE services with device name [{local_name}].')
      LOG.info(f'Adapter address: [{nus.ble_ctl.adapter_address}]')
      LOG.info(f'')
      LOG.info(f'  {run_as}')
      LOG.info(f'')
      LOG.info(f'Please connect to https://raw.githack.com/yjlou/ble_uart/master/examples/json_rpc/json_rpc.html')
      LOG.info(f'')
      LOG.info(f'Ctrl + C once you are done...')
      LOG.info(f'')
      threading.Event().wait()

    except Exception as err:
      LOG.error(f'Catch exception: {err}')
      LOG.info(f'Restarting ...')
      time.sleep(1)


if __name__ == '__main__':
  main()
