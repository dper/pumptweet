#!/usr/bin/env bash
cd `dirname $0`
source bin/activate
python PumpTweet.py
deactivate
