#!/usr/bin/env bash
set -e

ble_uart/pipeline_test.py

./ble_uart.py --dry_run
