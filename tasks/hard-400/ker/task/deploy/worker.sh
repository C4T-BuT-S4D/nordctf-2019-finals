#!/bin/sh

while true; do socat -d TCP4-LISTEN:33071,reuseaddr,fork,keepalive exec:./run_docker.sh; sleep 10; done
