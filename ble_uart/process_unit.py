#!/usr/bin/env python3
"""A Process Unit is a component that handles the data flows. It contains 2 flows:

  flow0: data flow from the BLE to the server side.
  flow1: data flow from the server side to the BLE.

        +--------------+
        | Process Unit |   S
        |              |   e
   B   ====> flow 0 ====>  r
   L    |              |   v
   E   <==== flow 1 <====  e
        |              |   r
        +--------------+
"""


class Flow(object):
  def __init__(self):
    self._egress = None

  def set_egress(self, egress:callable):
    self._egress = egress

  def ingress(self, data:bytearray):
    """This inputs data to the entrance of the flow.

    The default behavior is pass-thru. The inheritor can overwrite this.
    """
    if self._egress:
      self._egress(data)


class ProcessUnit(object):
  def __init__(self):
    self._flows = [Flow(), Flow()]

  def flow(self, idx:int):
    return self._flows[idx]
