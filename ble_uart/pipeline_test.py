#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from pipeline import Pipeline
import process_unit


class TestPipeline(unittest.TestCase):

  def test_three(self):
    # Set up the toppology, but not do anything yet.
    test_data = bytearray([1, 2, 3])
    pus = [process_unit.ProcessUnit(), process_unit.ProcessUnit(), process_unit.ProcessUnit()]
    pipeline = Pipeline(pus)

    # Setup the mockup functions.
    last_flow0 = MagicMock()
    first_flow1 = MagicMock()
    pus[2].flow(0).set_egress(last_flow0)
    pus[0].flow(1).set_egress(first_flow1)

    # The topology is not composed yet. The last PU will not be called.
    pus[0].flow(0).ingress(test_data)    
    last_flow0.assert_not_called()

    # Composed topology. Expect the last flow will be called.
    pipeline.compose()
    pus[0].flow(0).ingress(test_data)    
    last_flow0.assert_called_with(test_data)

    # Try the reversed flow.
    pus[2].flow(1).ingress(test_data)
    first_flow1.assert_called_with(test_data)


if __name__ == '__main__':
    unittest.main()
