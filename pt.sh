#!/usr/bin/env bash

# This must be placed at the base of virtualenv.
# It must be in the same directory as PumpTweet.ini.

source bin/activate
`dirname $0`/pt.py
deactivate
