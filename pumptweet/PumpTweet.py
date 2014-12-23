# coding=utf-8

from PumpLogin import PumpTweetParser
from pypump import PyPump
from MLStripper import strip_tags
from shorturl import shorten
from unicodedata import normalize
from pypump.models.collection import Public
import argparse

class PumpTweet(object):
	"""Cross-posts from Pump.io to Twitter."""

	# Connect to servers.
	def connect_to_servers(self):
		# Run the parser and grab useful values.
		self.ptp = PumpTweetParser()
		self.pump_me = self.ptp.get_pump_me()
		self.pump_username = self.ptp.get_pump_username()
		self.twitter_api = self.ptp.get_twitter_api()
	
	# Returns true if the activity is public.
	def ispublic(self, activity):
		recipients = []
		recipients += getattr(activity, 'to', [])
		recipients += getattr(activity, 'cc', [])
	
		for recipient in recipients:
			if recipient.id == Public.ENDPOINT:
				return True
		
		return False
	
	# Returns recent outbox activities.
	# If testing, don't stop at recent activity.
	def get_new_activities(self, testing=False):
		print 'Looking at Pump outbox activity...'
		
		# Some of this can be replaced by 'since' if later implemented by PyPump.
		published = self.ptp.get_published()
		recent = self.ptp.get_recent()
		outbox = self.pump_me.outbox
		history = self.ptp.get_history()
	
		# Users with a lot of non-note activity might raise this.
		count = 20
	
		# The maximum number of notes to post at a time.
		# Posting too frequently might lead to errors on Twitter.
		# If this number is too small, consider a more frequent cronjob.
		allowable_posts = 3
		notes = []
	
		for activity in outbox.major[:count]:
			print '> ' + activity.obj.objectType + ' (' + str(activity.published) + ')'
	
			# Stop looking at the outbox upon finding old activity.
			if history and not testing:
				if recent == activity.id: break
				if published >= activity.published: break
	
			# Only post several notes. Others are forgotten.
			if len(notes) >= allowable_posts: break
	
			# Only post public notes.
			if not self.ispublic (activity): break
	
			obj = activity.obj
	
			# Only post notes to Twitter.
			if obj.objectType != 'note': break
	
			# Skip deleted notes.
			if obj.deleted: break
	
			# Omit posts written by others and then shared.
			note_author = obj.author.id[len('acct:'):]
			if note_author != self.pump_username: break

			notes.append(obj)
		return notes
	
	# Make the text for a tweet that includes the contest of the note.
	def make_tweet(self, note):
		max_length = 136
		content = note.content
	
		# Convert or remove HTML.
		content = strip_tags(content)
	
		# If the note fits in a tweet, post it as-is.
		# Tweets of notes this short don't need to link to their source.
		if len(content.splitlines()) == 1 and len(content) <= max_length:
			return content
	
		# Make a short URL pointing to the original note.
		# Replace the middle of the private note URL to get a usable public link.
		private_url = note.id
		short_username = self.pump_username.split('@')[0]
		public_url = private_url.replace('/api/note/', '/' + short_username + '/note/')
		short_url = shorten(public_url)
	
		# Make room for the ellipsis and URL at the end of the tweet.
		cropped_length = max_length - len(short_url) - 2
	
		# Keep only the first line.
		content = content.splitlines()[0]
		content = content[:cropped_length]
		content = content.rstrip()
	
		tweet = content + u'… ' + short_url
		return tweet
	
	# Converts posts to tweets.
	def make_tweets(self, notes):
		tweets = []
		for note in notes:
			tweets.append(self.make_tweet(note))
		return tweets
	
	# Prints a list of tweets.
	def print_tweets(self, tweets):
		print 'Printing tweets...'
		for tweet in tweets:
			normal = normalize('NFKD', tweet).encode('ascii', 'ignore')
			print '> ' + normal
	
	# Posts a list of tweets.
	def post_tweets(self, tweets):
		print 'Posting to Twitter...'
		print 'New tweet count: ' + str(len(tweets)) + '.'
		for tweet in tweets:
			self.twitter_api.PostUpdate(tweet)
	
	# Updates the ini file with the most recent entry.
	def update_recent(self):
		print 'Updating history...'
		activity = self.pump_me.outbox.major[0]
		latest = activity.id
		published = activity.published
		self.ptp.update_recent(latest, published)
	
	# Pulls from Pump and produces text for some tweets.
	# Nothing is sent to Twitter. This is for testing.
	def pull_and_test(self):
		print 'Testing PumpTweet...'
		self.connect_to_servers()
		notes = self.get_new_activities(testing=True)
		tweets = self.make_tweets(notes)
		self.print_tweets(tweets)
	
	# Pulls from Pump and pushes to Twitter.
	def pull_and_push(self):
		self.connect_to_servers()
		notes = self.get_new_activities()
		tweets = self.make_tweets(notes)
		self.print_tweets(tweets)
		self.post_tweets(tweets)
		self.update_recent()
