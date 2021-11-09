# Cardinal (Ubuntu 18.04)

FROM ubuntu:bionic
MAINTAINER James McClune <jmcclune@mcclunetechnologies.net>
WORKDIR /opt

# Install dependencies & added extras
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git mysql-server mysql-client nginx sudo nano python3-venv locales python3-dev libmysqlclient-dev build-essential systemd

# Grab latest Cardinal source
RUN git clone https://github.com/cardinal-dev/Cardinal.git

# Set en_US.UTF-8 locale
RUN sudo locale-gen en_US.UTF-8
RUN sudo update-locale LANG=en_US.UTF-8

# Move Cardinal config to container
COPY nginx.conf /etc/nginx
COPY cardinal.service /etc/systemd/system
COPY wsgi.ini /opt/Cardinal/webapp

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
ENV CARDINALCONFIG=/home/cardinal.ini

# Run install.sh
RUN chmod +x /opt/Cardinal/bin/install.sh

# Finish it!
CMD ["/lib/systemd/systemd"]
