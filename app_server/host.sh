#!/bin/bash
socat -v tcp-l:$2,fork exec:"$1" >>~/socat.log 2>&1 &
