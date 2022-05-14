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

class TestCardinalAccessPoint(unittest.TestCase):
    '''
    Object for testing /api/v1/access_points endpoint.
    '''
    def config(self):
        '''
        Default config for TestCardinalAccessPoint() object
        '''
        self.apId = None

    def testCreateAccessPoint(self):
        '''
        Test POST'ing to /api/v1/access_points
        '''
        # HTTP POST form data
        data = dict(ap_name="Test1", ap_ip="192.168.2.210", ap_subnetmask="255.255.255.0", ssh_username="Cisco", ssh_password="Cisco", community="public")

        # POST to /api/v1/access_points
        origResponse = CardinalSessionHandler().post("/api/v1/access_points", data=data)[0]
        self.apId = origResponse["ap_id"]

        # Check response validity
        self.assertIn("ap_bandwidth", origResponse)
        self.assertIn("ap_group_id", origResponse)
        self.assertIn("ap_id", origResponse)
        self.assertIn("ap_ios_info", origResponse)
        self.assertIn("ap_ip", origResponse)
        self.assertIn("ap_location", origResponse)
        self.assertIn("ap_mac_addr", origResponse)
        self.assertIn("ap_model", origResponse)
        self.assertIn("ap_name", origResponse)
        self.assertIn("ap_serial", origResponse)
        self.assertIn("ap_ssh_username", origResponse)
        self.assertIn("ap_subnetmask", origResponse)
        self.assertIn("ap_total_clients", origResponse)
        self.assertIn("ap_uptime", origResponse)

        # Check values against API output
        self.assertEqual("Test1", origResponse["ap_name"])
        self.assertEqual("192.168.2.210", origResponse["ap_ip"])
        self.assertEqual("255.255.255.0", origResponse["ap_subnetmask"])
        self.assertEqual("Cisco", origResponse["ap_ssh_username"])
        
    def testGetAccessPointInfoById(self):
        '''
        Test GET'ing a single access point from /api/v1/access_points by id
        '''
        # HTTP POST form data
        data = dict(ap_name="Test2", ap_ip="192.168.2.211", ap_subnetmask="255.255.255.0", ssh_username="Cisco", ssh_password="Cisco", community="public")

        # POST to /api/v1/access_points
        postResponse = CardinalSessionHandler().post("/api/v1/access_points", data=data)[0]

        # GET access point data by ID
        getResponse = CardinalSessionHandler().get("/api/v1/access_points/{0}".format(self.apId))[0]

        # Check response validity
        self.assertIn("ap_bandwidth", getResponse)
        self.assertIn("ap_group_id", getResponse)
        self.assertIn("ap_id", getResponse)
        self.assertIn("ap_ios_info", getResponse)
        self.assertIn("ap_ip", getResponse)
        self.assertIn("ap_location", getResponse)
        self.assertIn("ap_mac_addr", getResponse)
        self.assertIn("ap_model", getResponse)
        self.assertIn("ap_name", getResponse)
        self.assertIn("ap_serial", getResponse)
        self.assertIn("ap_ssh_username", getResponse)
        self.assertIn("ap_subnetmask", getResponse)
        self.assertIn("ap_total_clients", getResponse)
        self.assertIn("ap_uptime", getResponse)

        # Check values against API output
        self.assertEqual("Test2", getResponse["ap_name"])
        self.assertEqual("192.168.2.211", getResponse["ap_ip"])
        self.assertEqual("255.255.255.0", getResponse["ap_subnetmask"])
        self.assertEqual("Cisco", getResponse["ap_ssh_username"])
        
    def testGetAllAccessPointInfo(self):
        '''
        Test GET'ing all access points from /api/v1/access_points
        '''
        response = CardinalSessionHandler().get("/api/v1/access_points")

        # Verify return list has greater than two elements
        self.assertGreater(len(response), 1)

    def testDeleteAccessPointByName(self):
        '''
        Test DELETE'ing an access point from /api/v1/access_points by name
        '''
        response = CardinalSessionHandler().delete("/api/v1/access_points", data=dict(ap_name="Test2"))

    def testDeleteAccessPointById(self):
        '''
        Test DELETE'ing an access point from /api/v1/access_points by id
        '''
        response = CardinalSessionHandler().delete("/api/v1/access_points", data=dict(ap_id=self.apId))

if __name__ == '__main__':
    unittest.main()