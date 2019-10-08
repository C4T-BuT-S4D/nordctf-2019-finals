#!/bin/bash

gcc -fno-stack-protector \
    -Wl,-z,noexecstack \
    -Wl,-z,relro,-z,now \
    -o kerable kerable.c
