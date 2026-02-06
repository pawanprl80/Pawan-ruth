#!/bin/bash
redis-server --daemonize yes
npm run build && npm run serve &
python3 gateway.py
