#!/bin/bash

mkdir -p /opt/hosts/presets
cp hosts.py hosts /opt/hosts
chmod +x /opt/hosts/hosts
ln /opt/hosts/hosts /usr/bin/hosts