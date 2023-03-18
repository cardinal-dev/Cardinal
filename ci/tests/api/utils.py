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

import os
import requests

class CardinalSessionHandler():
    '''
    Object that defines how Cardinal sends HTTP requests
    for CI testing.
    '''
    def __init__(self):
        '''
        Constructor for CardinalSessionHandler()
        '''
        # Authenticate to the Cardinal API
        cardinalCreds = {'username': os.environ["CARDINAL_USERNAME"], 'password': os.environ["CARDINAL_PASSWORD"]}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.cardinalSession = requests.Session()
        self.cardinalSession.post("http://127.0.0.1/login", data=cardinalCreds, headers=headers)

    def get(self, endpoint):
        '''
        Send a GET request to Cardinal using provided credentials.
        '''
        return self.cardinalSession.get("http://127.0.0.1{0}".format(endpoint)).json()

    def post(self, endpoint, data):
        '''
        Send a POST request to Cardinal using provided credentials.
        '''
        return self.cardinalSession.post("http://127.0.0.1{0}".format(endpoint), data=data).json()

    def delete(self, endpoint, data):
        '''
        Send a POST request to Cardinal using provided credentials.
        '''
        return self.cardinalSession.delete("http://127.0.0.1{0}".format(endpoint), data=data).json()