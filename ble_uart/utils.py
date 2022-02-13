#!/usr/bin/env python3
"""
"""
import logging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger()

# The BLE data use |bytearray|. Thus, please convert data for BLE stack to |bytearray|.
#
def str_to_bytearray(value:str):
  assert isinstance(value, str)

  # When hanlding the console input, the input can be converted to Unicode, which the
  # ord() cannot support. When this happens, convert it to utf-8.
  out = []
  for ch in value:
    out += ch.encode('utf-8') if ord(ch) >= 256 else [ord(ch)]

  return bytearray(out)

def str_to_list(value:str):
  assert isinstance(value, str)
  return [ord(x) for x in value]

# Same here. Convert integer into bytearray for the BLE stack (little-endian).
#
def byte_to_bytearray(value:int):
  assert isinstance(value, int)
  return list(int(value).to_bytes(1, byteorder='little', signed=True))

# Convert data from BLE stack.
#
def bytearray_to_str(blist:list):
  return bytearray(blist).decode('utf-8')
