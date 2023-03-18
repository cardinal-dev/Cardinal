#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2022 Cardinal Contributors

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

import time
import subprocess
from cardinal.system.common import ToolkitJob

def ping(hostname, count=4):
    '''
    Function that invokes subprocess
    to execute ping
    '''
    returnDict = dict()

    # Initialize ToolkitJob() object
    jobRecord = ToolkitJob()

    pingArgs = ["ping", "-c", str(count), str(hostname)]
    startTime = time.time()
    executePing = subprocess.Popen(pingArgs, stdout=subprocess.PIPE)
    pingResult = executePing.stdout.read()
    endTime = time.time()
    
    returnDict["command"] = "ping"
    returnDict["arguments"] = str(pingArgs)
    returnDict["duration"] = endTime - startTime
    returnDict["result"] = pingResult.decode('ascii')

    # Commit job record to MariaDB backend
    jobRecord.add(command=returnDict["command"], arguments=returnDict["arguments"], duration=returnDict["duration"], \
                result=returnDict["result"])

    return returnDict

def traceroute(hostname):
    '''
    Function that invokes subprocess
    to execute traceroute
    '''
    returnDict = dict()

    # Initialize ToolkitJob() object
    jobRecord = ToolkitJob()

    tracertArgs = ["traceroute", str(hostname)]
    startTime = time.time()
    executeTracert = subprocess.Popen(tracertArgs, stdout=subprocess.PIPE)
    tracertResult = executeTracert.stdout.read()
    endTime = time.time()
    
    returnDict["command"] = "traceroute"
    returnDict["arguments"] = str(tracertArgs)
    returnDict["duration"] = endTime - startTime
    returnDict["result"] = tracertResult.decode('ascii')

    # Commit job record to MariaDB backend
    jobRecord.add(command=returnDict["command"], arguments=returnDict["arguments"], duration=returnDict["duration"], \
                result=returnDict["result"])

    return returnDict

def dig(hostname):
    '''
    Function that invokes subprocess
    to execute dig
    '''
    returnDict = dict()

    # Initialize ToolkitJob() object
    jobRecord = ToolkitJob()

    digArgs = ["dig", str(hostname)]
    startTime = time.time()
    executeDig = subprocess.Popen(digArgs, stdout=subprocess.PIPE)
    digResult = executeDig.stdout.read()
    endTime = time.time()
    
    returnDict["command"] = "dig"
    returnDict["arguments"] = str(digArgs)
    returnDict["duration"] = endTime - startTime
    returnDict["result"] = digResult.decode('ascii')

    # Commit job record to MariaDB backend
    jobRecord.add(command=returnDict["command"], arguments=returnDict["arguments"], duration=returnDict["duration"], \
                result=returnDict["result"])

    return returnDict

def curl(hostname):
    '''
    Function that invokes subprocess
    to execute curl
    '''
    returnDict = dict()

    # Initialize ToolkitJob() object
    jobRecord = ToolkitJob()

    curlArgs = ["curl", "-Is", str(hostname)]
    startTime = time.time()
    executeCurl = subprocess.Popen(curlArgs, stdout=subprocess.PIPE)
    curlResult = executeCurl.stdout.read()
    endTime = time.time()

    returnDict["command"] = "curl"
    returnDict["arguments"] = str(curlArgs)
    returnDict["duration"] = endTime - startTime
    returnDict["result"] = curlResult.decode('ascii')

    # Commit job record to MariaDB backend
    jobRecord.add(command=returnDict["command"], arguments=returnDict["arguments"], duration=returnDict["duration"], \
                result=returnDict["result"])

    return returnDict