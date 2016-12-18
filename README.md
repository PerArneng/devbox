# devbox
This repository contains scripts and configuration files to setup a linux development machine.

# Supported distributions
* Ubuntu 16.10

# install devbox
```
$ sudo pip install -e git+git@github.com:PerArneng/devbox.git#egg=devbox
```

# Example
```
 $ devbox -a tmux
```

# Run on Windows
```
$ docker run -v c:/Users/perar:/home/devbox/hosthome -u devbox -it perarneng/devbox /bin/bash
```