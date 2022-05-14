#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2023 Cardinal Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from utils import CardinalSessionHandler
import unittest

class TestCardinalMetricsEndpoint(unittest.TestCase):
    '''
    Object for testing /api/v1/metrics endpoint and
    overall Cardinal API functionality.
    '''
    def testMetricsEndpoint(self):
        '''
        Test GET'ing information from /api/v1/metrics
        '''
        # Test Cardinal API health by hitting the /api/v1/metrics endpoint
        metricFetch = CardinalSessionHandler().get("/api/v1/metrics")

        # Check response validity
        self.assertIn("access_point_groups", metricFetch)
        self.assertIn("access_points", metricFetch)
        self.assertIn("ssids_24ghz", metricFetch)
        self.assertIn("ssids_24ghz_radius", metricFetch)
        self.assertIn("ssids_5ghz", metricFetch)
        self.assertIn("ssids_5ghz_radius", metricFetch)
        self.assertIn("total_clients", metricFetch)
        self.assertIn("total_ssids", metricFetch)

        # TODO: Add check for integer return value and HTTP response codes

if __name__ == '__main__':
    unittest.main()