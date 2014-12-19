#!/bin/sh
cd `dirname $0`
source bin/activate
python PumpTweet.py
deactivate
