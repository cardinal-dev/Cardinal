#!/bin/bash

# Cardinal - An Open Source Cisco Wireless Access Point Controller

# MIT License

# Copyright © 2019 Cardinal Contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# The purpose of this script is to start a standalone (development) container of Cardinal. 
# If you want to customize more of the build process, please reference the resources within webapp/docker.

# Build Cardinal container

echo "INFO: Starting initial docker build..."
docker build -t cardinal_build .
dockerBuildStatus=$(echo $?)

# Start Cardinal container process

if [ "$dockerBuildStatus" = 0 ]; then
    echo "INFO: Starting Cardinal container based on cardinal_build image..."
    docker run -d --privileged --name cardinal_build -v /sys/fs/cgroup:/sys/fs/cgroup:ro cardinal_build
    dockerRunStatus=$(echo $?)
else
    echo "ERROR: docker build failed. Please check the docker build stdout/stderr for more information."
    exit 1
fi

if [ "$dockerRunStatus" = 0 ]; then
    echo "INFO: Executing install.sh on Cardinal container..."
    docker exec -it cardinal_build /bin/bash /opt/Cardinal/bin/install.sh --run 127.0.0.1 root testing1234 cardinal admin admin /home /opt/Cardinal/lib/scout/templates 704cc365c40c8b2ebebe
    runInstallStatus=$(echo $?)
else
    echo "ERROR: Cardinal container could not be made. Please check stdout/stderr for more information."
    exit 1
fi

if [ "$runInstallStatus" = 0 ]; then
    echo "INFO: Running docker commit on Cardinal container..."
    imageCommit=$(docker commit cardinal_build)
    dockerCommitStatus=$(echo $?)
else
    echo "ERROR: install.sh failed. Please check stdout/stderr for more information."
    exit 1
fi

if [ "$dockerCommitStatus" = 0 ]; then
    echo "INFO: Removing old cardinal artifacts..."
    dockerImage=$(echo "$imageCommit" | tr -d ":" | sed -e 's/sha256//g' | cut -c 1-12)
    docker tag "$dockerImage" cardinal
    docker rm -f cardinal_build
    docker rmi cardinal_build
    docker run -d -p 1000:80 --privileged --name cardinal -v /sys/fs/cgroup:/sys/fs/cgroup:ro cardinal
    echo "INFO: Starting Cardinal..."
    docker exec -it cardinal systemctl restart cardinal
else
    echo "ERROR: docker commit failed. Please check stdout/stderr for more information."
    exit 1
fi
