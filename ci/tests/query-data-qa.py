#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2019 Cardinal Contributors

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

# THIS IS ONLY A TEST FILE!

import pathlib
import re

# Test querying AP model

with pathlib.Path("ci/templates/version").open(mode='r') as file:
    apModelRegex = re.compile(r'\w\w\w\-\w\w\w\w\w\w\w\w\-\w-\w\w')
    getModelString = file.read().replace("\n", '')
    getApModel = apModelRegex.search(getModelString).group(0)
    print("--get-model OUTPUT RESULT: {}".format(getApModel))

# Test querying MAC address

with pathlib.Path("ci/templates/interface").open(mode='r') as file:
    macAddrRegex = re.compile(r'\w\w\w\w.\w\w\w\w.\w\w\w\w')
    getMacString = file.read().replace("\n", '')
    getMacList = getMacString.split(",")
    getMac = macAddrRegex.search(getMacList[2]).group(0)
    print("--get-mac OUTPUT RESULT: {}".format(getMac))

# Test querying AP speed

with pathlib.Path("ci/templates/interface").open(mode='r') as file:
    getSpeedString = file.read().replace("\n", '')
    getSpeedList = getSpeedString.split(",")
    getSpeed = getSpeedList[9].strip("Mbps")
    print("--get-speed OUTPUT RESULT: {}".format(getSpeed))

