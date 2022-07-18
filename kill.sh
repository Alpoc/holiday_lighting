#!/bin/bash
kill $(ps aux | grep '[p]ython run.py' | awk '{print $2}')
sudo python off.py
