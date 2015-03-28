# devbox
This repository contains scripts and configuration files to setup a linux development machine. It uses ansible underneath to connect to a remote host and set it up using ansible tasks. Ansible normally manages multiple hosts but this scripts makes it one at a time by creating a temporary inventory file consisting of the hostname given as the *remote_host* argument of the the script.

# Supported distributions
* Ubuntu 14.04 LTS

# Example
```
 $ bash install_devbox.sh -u rupert -r 123.43.21.143
```
