#!/usr/bin/env python3
"""The main program
"""
import argparse
import os
import sys
import threading
import time

sys.path.append(os.path.realpath('./'))  # to import file in the current directory.
sys.path.append(os.path.realpath('./ble_uart'))  # to import file in the ble_uart directory.

import ble_uart.echo
import ble_uart.exec
import ble_uart.file_io
from ble_uart.nus import Nus
from ble_uart.pipeline import Pipeline
import ble_uart.utils
from ble_uart.utils import LOG


PARSER = argparse.ArgumentParser()
PARSER.add_argument('--dry_run', dest='dry_run', action='store_true', default=False,
                    help='Dry run. Don\'t do nothing.')
PARSER.add_argument('-e', '--echo', dest='echo', action='store_true', default=False,
                    help='Launch echo server')
PARSER.add_argument('-l', '--login', dest='login', action='store_true', default=False,
                    help='Use /bin/login')
PARSER.add_argument('-n', '--name', dest='name', type=str, default=None,
                    help='The BLE device name')
PARSER.add_argument('-c', '--command', dest='command', type=str, default=None,
                    help='Run command')
PARSER.add_argument('-r', '--read', dest='read', type=str, default='/dev/stdin',
                    help='Read from a file')
PARSER.add_argument('-w', '--write', dest='write', type=str, default='/dev/stdout',
                    help='Write to a file')


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
      if args.echo:
        run_as = f'Launch Echo server'
        echo = ble_uart.echo.Echo()
        late_bind.set(echo.start, echo.stop)
        pipeline = Pipeline([nus, echo])

      elif args.login:
        run_as = f'Login to console'
        exec = ble_uart.exec.Exec('/bin/login')
        late_bind.set(exec.start, exec.stop)
        pipeline = Pipeline([nus, exec])

      elif args.command:
        run_as = f'Run command'
        exec = ble_uart.exec.Exec(args.command)
        late_bind.set(exec.start, exec.stop)
        pipeline = Pipeline([nus, exec])

      else:
        run_as = f'File IO'
        file_io = ble_uart.file_io.FileIo(args.read, args.write)
        late_bind.set(file_io.start, file_io.stop)
        pipeline = Pipeline([nus, file_io])

      pipeline.compose()
      nus.start()

      LOG.info(f'Created BLE services with device name [{local_name}].')
      LOG.info(f'Adapter address: [{nus.ble_ctl.adapter_address}]')
      LOG.info(f'')
      LOG.info(f'  {run_as}')
      LOG.info(f'')
      LOG.info(f'Please use your phone to connect and try to read/write the services.')
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
