#!/usr/bin/env python
# coding=utf-8

import argparse
from pumptweet import PumpTweet

if __name__ == "__main__":
	description = 'Cross-post from pump to twitter.  Call with no options for normal use.'
	test_help = 'do a test-run without tweeting'
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-t', '--test', help=test_help, action='store_true')
	args = parser.parse_args()
	pumptweet = PumpTweet.PumpTweet()
	
	if args.test:
		pumptweet.pull_and_test()
	else:
		pumptweet.pull_and_push()
