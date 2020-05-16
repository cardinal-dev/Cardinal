<h1>Running Cardinal in a Docker Container</h1>

If desired, Cardinal can be deployed in a Docker container. Containers allow you
to deploy applications in an isolated environment, acting as tenants to the Linux
guest.

The `Dockerfile` provided installs the latest Cardinal source within an Ubuntu 18.04
environment. Before building the Cardinal image, please make sure you adapt the `Dockerfile`
to fit your needs (i.e. locale, environment variables, etc.).

The default `Dockerfile` will install Cardinal using the `en_US` locale and sets
`CARDINALCONFIG` to `/home/cardinal.ini`. Please make sure you know where the `.ini`
file will be stored before building, so the environment variable is properly configured.
If you want to try Cardinal in a development environment, just keep the defaults
and then run `install.sh` from either outside or inside the container. If you're going to
use `install.sh`, please make sure you run it from the origin directory (i.e. `bin/`). `build-container.sh`
is a very simplified method of starting up a Cardinal container, if you want a quick demo environment.

To use the default config, please follow these steps:

1.) Please make sure you have Docker installed. For more information on installing Docker, please
reference this [link](https://docs.docker.com/install/).

2.) Once you have Docker installed, please pull the Cardinal code from GitHub
and navigate to the `webapp/docker` directory.

3.) As stated above, please make sure the associated files are properly configured (depending on 
your environment). If you're using the default test config, you can skip this step.

4.) Run `docker build -t cardinal .` from the `webapp/docker` directory in order
to build the `cardinal` image.

5.) Once the image has been built successfully, you can create a container from that image
using the following command:

~~~
docker run -d -p <OUTSIDE_PORT>:<INSIDE_PORT> --privileged --name cardinal -v /sys/fs/cgroup:/sys/fs/cgroup:ro cardinal
docker run -d -p 1000:80 --privileged --name cardinal -v /sys/fs/cgroup:/sys/fs/cgroup:ro cardinal
~~~

The preceding command will create a Docker container named `cardinal` and will map an external host port to one of the 
container's internal ports. For example, the Cardinal UI is served on HTTP (i.e. `80/tcp`) by default. You can specify a port that the host has available 
to allow external access to Cardinal.

6.) Once you have the container running, please run `install.sh` in order to finalize the Cardinal environment. You can do this by executing
the following commands from inside the container.

~~~
docker exec -it cardinal /bin/bash
cd Cardinal/bin
chmod +x install.sh
./install.sh
~~~

7.) Running `install.sh` should trigger the install process. Please answer the prompts accordingly.

8.) If `install.sh` finishes successfully with no errors (other than MySQL warnings about insecure password on CLI), please make sure
you restart the Cardinal service:

~~~
docker exec -it cardinal systemctl restart cardinal
~~~

9.) After restarting the Cardinal service, the UI should now be available at `http://<DOCKER_HOST>:<EXTERNAL_PORT>`.

If you have any difficulties during this process or need further clarification, please open an issue report on Cardinal's GitHub
repository.
