#!/bin/sh
while true; do
    curl -s -x socks://localhost:9050 http://ipecho.net/plain
    echo
done
