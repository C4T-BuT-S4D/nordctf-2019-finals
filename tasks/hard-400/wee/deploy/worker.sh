while true; do socat -d TCP4-LISTEN:33074,reuseaddr,fork,keepalive exec:./run_docker.sh; sleep 10; done
