#!/bin/bash

CGO_ENABLED=0 /usr/local/go/bin/go build -v -a -ldflags="-w" -gcflags="all=-trimpath=/tmp/gorevad" -asmflags="all=-trimpath=/tmp/gorevad" -o malware .