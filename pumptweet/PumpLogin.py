from pypump import PyPump
from pypump import Client
from dateutil.parser import parse
from ConfigParser import SafeConfigParser
import twitter
import os.path

def simple_verifier(url):
	print 'Please follow the instructions at the following URL:'
	print url
	return raw_input("Verifier: ") # the verifier is a string

class PumpTweetParser:
	"""Parses the ini file and provides the results on demand."""

	# This file must exist in the current directory.
	filename = 'PumpTweet.ini'


	# Parses the ini file.
	def parse_ini(self):
		print 'Reading the config file...'

		# This verifies that the ini file exists.
		if not os.path.isfile(self.filename):
			message = self.filename + ' not found.'
			raise Exception(message)

		parser = SafeConfigParser()
		parser.read(self.filename)
		self._parser = parser
		self._recent = parser.get('history', 'recent')

		# Converts the date to a usable form.
		date = parser.get('history', 'published')
		self._published = parse(date)

		# Notes whether history exists in the ini file.
		self._history = len(date) > 0 and len(self._recent) > 0

	# Logs in to the Pump server.
	def pump_login(self):
		print 'Logging into the Pump server...'

		username = self._parser.get('pump', 'username')
		key = self._parser.get('pump', 'key')
		secret = self._parser.get('pump', 'secret')
		token = self._parser.get('pump', 'token')
		token_secret = self._parser.get('pump', 'token_secret')

		client = Client(
			webfinger = username,
			name = "Pump.io",
			type = "native",
			key = key,
			secret = secret)

		pump = PyPump(
			client = client,
			token = token,
			secret = token_secret,
			verifier_callback = simple_verifier)

		me = pump.Person(username)
		
		self._username = username
		self._pump = pump
		self._me = me

	# Logs in to Twitter.
	def twitter_login(self):
		print 'Logging into Twitter...'
		key = self._parser.get('twitter', 'key')
		secret = self._parser.get('twitter', 'secret')
		token = self._parser.get('twitter', 'token')
		token_secret = self._parser.get('twitter', 'token_secret')
		api = twitter.Api(
			consumer_key=key,
			consumer_secret=secret,
			access_token_key=token,
			access_token_secret=token_secret
		)
		
		self._api = api

	def __init__(self):
		self.parse_ini()
		self.pump_login()
		self.twitter_login()

	# Writes the latest update Pump ID in the ini file.
	# Be careful when changing this.  It rewrites the ini file.
	def update_recent(self, latest, published):
		self._parser.set('history', 'recent', latest)
		self._parser.set('history', 'published', str(published))

		with open(self.filename, 'wb') as inifile:
			self._parser.write(inifile)

	# Returns the ID for the last update (from the ini file).
	def get_recent(self):
		return self._recent

	# Returns the datetime of the last update (from the ini file).
	def get_published(self):
		return self._published

	# Returns True iff there is valid history (from the ini file).
	def get_history(self):
		return self._history

	# Returns the Pump user object.
	def get_pump_me(self):
		return self._me

	# Returns the Twitter user object.
	def get_twitter_api(self):
		return self._api

	# Returns the pump username.
	def get_pump_username(self):
		return self._username
