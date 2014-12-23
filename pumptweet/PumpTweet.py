# coding=utf-8

from PumpLogin import PumpTweetParser
from pypump import PyPump
from MLStripper import strip_tags
from shorturl import shorten
from unicodedata import normalize
from pypump.models.collection import Public
import argparse

# Connect to servers.
def connect_to_servers():
	# Run the parser and grab useful values.
	global __ptp__
	global __pump_me__
	global __pump_username__
	global __twitter_api__
	__ptp__ = PumpTweetParser()
	__pump_me__ = __ptp__.get_pump_me()
	__pump_username__ = __ptp__.get_pump_username()
	__twitter_api__ = __ptp__.get_twitter_api()

# Returns true if the activity is public.
def ispublic(activity):
	recipients = []
	recipients += getattr(activity, 'to', [])
	recipients += getattr(activity, 'cc', [])

	for recipient in recipients:
		if recipient.id == Public.ENDPOINT:
			return True
	
	return False

# Returns recent outbox activities.
# If testing, don't stop at recent activity.
def get_new_activities(testing=False):
	print 'Looking at Pump outbox activity...'
	
	# Some of this can be replaced by 'since' if later implemented by PyPump.
	published = __ptp__.get_published()
	recent = __ptp__.get_recent()
	outbox = __pump_me__.outbox
	history = __ptp__.get_history()

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
		if not ispublic (activity): break

		obj = activity.obj

		# Only post notes to Twitter.
		if obj.objectType != 'note': break

		# Skip deleted notes.
		if obj.deleted: break

		# Omit posts written by others and then shared.
		note_author = obj.author.id[len('acct:'):]
		if note_author != __pump_username__: break

		notes.append(obj)
	return notes

# Make the text for a tweet that includes the contest of the note.
def make_tweet(note):
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
	short_username = __pump_username__.split('@')[0]
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
def make_tweets(notes):
	tweets = []
	for note in notes:
		tweets.append(make_tweet(note))
	return tweets

# Prints a list of tweets.
def print_tweets(tweets):
	print 'Printing tweets...'
	for tweet in tweets:
		normal = normalize('NFKD', tweet).encode('ascii', 'ignore')
		print '> ' + normal

# Posts a list of tweets.
def post_tweets(tweets):
	print 'Posting to Twitter...'
	print 'New tweet count: ' + str(len(tweets)) + '.'
	for tweet in tweets:
		__twitter_api__.PostUpdate(tweet)

# Updates the ini file with the most recent entry.
def update_recent():
	print 'Updating history...'
	activity = __pump_me__.outbox.major[0]
	latest = activity.id
	published = activity.published
	__ptp__.update_recent(latest, published)

# Pulls from Pump and produces text for some tweets.
# Nothing is sent to Twitter. This is for testing.
def pull_and_test():
	print 'Testing PumpTweet...'
	connect_to_servers()
	notes = get_new_activities(testing=True)
	tweets = make_tweets(notes)
	print_tweets(tweets)

# Pulls from Pump and pushes to Twitter.
def pull_and_push():
	connect_to_servers()
	notes = get_new_activities()
	tweets = make_tweets(notes)
	print_tweets(tweets)
	post_tweets(tweets)
	update_recent()

description = 'Cross-post from pump to twitter.  Call with no options for normal use.'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-t', '--test', help='do a test-run without actually tweeting', action='store_true')
args = parser.parse_args()

if args.test:
	pull_and_test()
else:
	pull_and_push()
