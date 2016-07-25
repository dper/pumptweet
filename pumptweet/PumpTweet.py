# coding=utf-8

from .PumpLogin import PumpTweetParser
from pypump import PyPump
from .MLStripper import strip_tags
from unicodedata import normalize
from pypump.models.collection import Public
from twitter import TwitterError
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
	def is_public(self, activity):
		recipients = []
		recipients += getattr(activity, 'to', [])
		recipients += getattr(activity, 'cc', [])
		public_id = Public().id
	
		for recipient in recipients:
			if recipient.id == public_id:
				return True
	
		return False
	
	# Returns recent outbox activities.
	# If testing, don't stop at recent activity.
	def get_new_activities(self):
		print('Looking at Pump outbox activity...')
		
		# Some of this can be replaced by 'since' if later implemented by PyPump.
		outbox = self.pump_me.outbox
		history = self.ptp.get_history()
	
		# Users with a lot of non-note activity might raise this.
		count = 20
	
		# The maximum number of notes to post at a time.
		# Posting too frequently might lead to errors on Twitter.
		# If this number is too small, consider a more frequent cronjob.
		allowable_posts = 3
		posts = []
	
		# Returns true if the script has already run since the activity happened.
		def is_old(activity):
			# If there's no logged history, activities are new.
			if not history: return False

			published = self.ptp.get_published()
			recent = self.ptp.get_recent()
			return recent == activity.id or published >= activity.published

		# Returns true if the activity is something we should cross-post.
		def is_crosspostable(activity):
			obj = activity.obj
			obj_type = obj.object_type
			note_author = obj.author.id[len('acct:'):]

			if not self.is_public(activity): return False
			if obj.deleted: return False
			if note_author != self.pump_username: return False

			return obj_type == 'note' or obj_type == 'image'

		for activity in outbox.major[:count]:
			print('> ' + activity.obj.object_type + ' (' + str(activity.published) + ')')

			# Stop looking at the outbox upon finding old activity.
			if is_old(activity) and not self.testing: break
	
			# Only post several notes. Others are forgotten.
			if len(posts) >= allowable_posts: break

			# Only the right kind of activities are cross-posted.
			if is_crosspostable(activity):
				posts.append(activity.obj)

		return posts
	
	# Prints a list of tweets.
	def print_tweet(self, tweet):
		print("---------------------------------\n")
		normal = normalize('NFKD', tweet).encode('ascii', 'ignore')
		print('> ' + normal.decode('ascii'))
	
	# Make the text for a tweet that includes the content of the note.
	def make_text(self, note):
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
	
		# Make room for the ellipsis and URL at the end of the tweet.
		# Note that all links on Twitter are shortened via t.co. Therefore, all links
		# are 22 or 23 characters, depending on whether they use HTTP or HTTPS.
		cropped_length = max_length - 23 - 2
	
		# Keep only the first line.
		content = content.splitlines()[0]
		content = content[:cropped_length]
		content = content.rstrip()

		text = content + u'… ' + public_url	
		return text

	# Posts a note.
	def post_note(self, post):
		text = self.make_text(post)
		self.print_tweet(text)

		if self.testing: return

		try:
			self.twitter_api.PostUpdates(text)
		except TwitterError as e:
			print('---------------------------------')
			print('Twitter error.')
			print(e)
			print('---------------------------------')

			if self.halt_on_error:
				raise

	# Posts an image.
	def post_image(self, post):
		text = self.make_text(post)
		self.print_tweet(text)
		url = post.original.url

		if self.testing: return

		try:
			self.twitter_api.PostUpdate(text, media=url)
		except TwitterError as e:
			print('---------------------------------')
			print('Twitter error.')
			print(e)
			print('---------------------------------')

			if self.halt_on_error:
				raise

	# Makes and posts tweets.
	def post_all(self, posts):
		print('New tweet count: ' + str(len(posts)) + '.')

		for post in posts:
			obj_type = post.object_type

			if obj_type == 'note':
				self.post_note(post)
			elif obj_type == 'image':
				self.post_image(post)

	# Updates the ini file with the most recent entry.
	def update_recent(self):
		print('Updating history...')
		activity = self.pump_me.outbox.major[0]
		latest = activity.id
		published = activity.published
		self.ptp.update_recent(latest, published)
	
	# Pulls from Pump and produces text for some tweets.
	# Nothing is sent to Twitter. This is for testing.
	def pull_and_test(self):
		print('Testing PumpTweet...')
		self.testing = True
		self.connect_to_servers()
		posts = self.get_new_activities()
		self.post_all(posts)
	
	# Pulls from Pump and pushes to Twitter.
	#
	# The parameter halt_on_error affects error handling.
	# By default, we show the error message but continue on.
	def pull_and_push(self, halt_on_error=False):
		self.testing = False
		self.halt_on_error = halt_on_error
		self.connect_to_servers()
		posts = self.get_new_activities()
		self.post_all(posts)
		self.update_recent()
