from PumpLogin import PumpTweetParser
from pypump import PyPump
from MLStripper import strip_tags
from shorturl import shorten

# Run the parser and grab useful values.
ptp = PumpTweetParser()
pump_me = ptp.get_pump_me()
twitter_api = ptp.get_twitter_api()

# Returns recent outbox activities.
def get_new_activities():
	print 'Looking at Pump outbox activity...'
	
	# Some of this can be replaced by 'since' if later implemented by PyPump.
	published = ptp.get_published()
	recent = ptp.get_recent()
	outbox = pump_me.outbox

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
		#if recent == activity.id: break
		#if published >= activity.published: break

		# Only post several notes. Others are forgotten.
		#if len(notes) >= allowable_posts: break

		obj = activity.obj

		# Only post notes to Twitter.
		if obj.objectType == 'note' and obj.deleted == False:
			notes.append(obj)
	return notes

# Make the text for a tweet that includes the contest of the note.
def make_tweet(note):
	max_length = 140

	opener = ''
	closer = '... '

	private_url = note.id
	public_url = private_url.replace('/api/note/', '/dper/note/')
	short_url = shorten(public_url)

	remaining_length = max_length - len(opener) - len(short_url) - len(closer) - 3
	
	content = note.content[3:]		# Strip leading characters.
	content = content.replace('&#39;', "'")	# Replace HTML apostrophes.
	content = strip_tags(content)		# Strip HTML.
	content = content.splitlines()[0]	# Keep only the first line.
	content = content.strip()		# Strip white space.
	content = content[:remaining_length]	# Shorten to 140 characters.

	tweet = opener + content + closer + short_url
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
		print '> ' + tweet

# Posts a list of tweets.
def post_tweets(tweets):
	print 'Posting to Twitter...'
	print 'New tweet count: ' + str(len(tweets)) + '.'
	for tweet in tweets:
		twitter_api.PostUpdate(tweet)

# Updates the ini file with the most recent entry.
def update_recent():
	print 'Updating history...'
	activity = pump_me.outbox.major[0]
	latest = activity.id
	published = activity.published
	ptp.update_recent(latest, published)

# Pulls from Pump and pushes to Twitter.
def pull_and_push():
	notes = get_new_activities()
	tweets = make_tweets(notes)
	print_tweets(tweets)
	#post_tweets(tweets)
	update_recent()

pull_and_push()
