from PumpLogin import PumpTweetParser
from pypump import PyPump
from MLStripper import strip_tags
from shorturl import shorten

# Run the parser and grab useful values.
ptp = PumpTweetParser()
pump_me = ptp.get_pump_me()
twitter_api = ptp.get_twitter_api()

# Returns recent outbox activities.
def get_recent_outbox_activities(count):
	print 'Looking at recent pump.io outbox activity...'
	notes = []

	#TODO This needs to only grab stuff since a certain ID.
	# Waiting on https://github.com/xray7224/PyPump/issues/67
	# ptp.get_recent stores the ID last used.

	outbox = pump_me.outbox
	for activity in outbox.major[:count]:
		obj = activity.obj
		if obj.objectType == 'note' and obj.deleted == False:
			notes.append(obj)
	return notes

# Make the text for a tweet that includes the contest of the note.
def make_tweet(note):
	max_length = 140

	opener = 'Microca.st: '
	closer = '... '

	private_url = note.id
	public_url = private_url.replace('/api/note/', '/dper/note/')
	short_url = shorten(public_url)

	remaining_length = max_length - len(opener) - len(short_url) - len(closer) - 2
	
	content = note.content[3:]		# Strip leading characters.
	content = content.replace('&#39;', "'")	# Replace HTML apostrophes.
	content = strip_tags(content)		# Strip HTML.
	content = content.splitlines()[0]	# Keep only the first line.
	content = content.strip()		# Strip white space.
	content = content[:remaining_length]	# Shorten to 140 characters.

	tweet = opener + content + closer + short_url
	return tweet

# Converts posts to tweets.
def make_tweets(count):
	print 'Converting posts to tweets...'
	tweets = []
	notes = get_recent_outbox_activities(2 * count)
	for note in notes[:count]:
		tweets.append(make_tweet(note))
	return tweets

# Posts a list of tweets.
def post_tweets(tweets):
	print 'Posting to Twitter...'
	for tweet in tweets:
		print len(tweet)
		twitter_api.PostUpdate(tweet)

# Updates the ini file with the most recent entry.
def update_recent():
	print 'Updating history...'
	activity = pump_me.outbox.major[0]
	activity_id = activity.id
	ptp.update_recent(activity_id)

tweets = make_tweets(4)
#post_tweets(tweets)
update_recent()
