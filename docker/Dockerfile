FROM ubuntu:16.10
MAINTAINER Per Arneng

RUN apt-get -qq update && \
    apt-get -q -y upgrade && \
    apt-get install -y sudo curl wget locales ansible git python-pip && \
    rm -rf /var/lib/apt/lists/*

# Ensure that we always use UTF-8 and with US English locale
RUN locale-gen en_US.utf8

COPY ./default_locale /etc/default/locale
RUN chmod 0755 /etc/default/locale

RUN useradd -m -p xxx -s /bin/bash devbox
RUN echo devbox:devbox | chpasswd
RUN sudo adduser devbox sudo

RUN mkdir /home/devbox/hosthome
WORKDIR /home/devbox/hosthome


#RUN sudo pip install -e git+git@github.com:PerArneng/devbox.git#egg=devbox

