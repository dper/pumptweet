#!/usr/bin/env python3
# coding=utf-8

import argparse
from pumptweet import PumpTweet

if __name__ == "__main__":
	description = 'Cross-post from pump to twitter.  Call with no options for normal use.'
	test_help = 'do a test-run without tweeting'
	halt_help = 'halt on Twitter length error'
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-t', '--test', help=test_help, action='store_true')
	parser.add_argument('-e', '--halt_on_error', help=halt_help, action='store_true')
	args = parser.parse_args()
	pumptweet = PumpTweet.PumpTweet()
	
	if args.test:
		pumptweet.pull_and_test()
	else:
		halt_on_error = True if args.halt_on_error else False
		pumptweet.pull_and_push(halt_on_error=halt_on_error)
