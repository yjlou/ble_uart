#!/usr/bin/env python3
"""Pipeline is a kind of topology.

Given a list of ProcessUnit, this class composes a pipeline topology. The first ProcessUnit's
flow0 output will be forwarded to the second ProcessUnit's flow0 input, and so on. The last
ProcessUnit's flow1 output will be forwarded to the last 2nd ProcessUnit's flow1 input... etc.

"""

class Pipeline(object):
  def __init__(self, process_units):
    """Constructor.

    Args:
      process_units: array of ProcessUnit
    """
    self._process_units = process_units

  def compose(self):
    assert len(self._process_units) >= 2

    # forwarding...
    for i in range(len(self._process_units) - 1):
      self._process_units[i].flow(0).set_egress(self._process_units[i + 1].flow(0).ingress)

    # backwarding ...
    for i in range(len(self._process_units) - 1, 0, -1):
      self._process_units[i].flow(1).set_egress(self._process_units[i - 1].flow(1).ingress)
