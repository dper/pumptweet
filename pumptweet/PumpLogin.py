import os.path
import sys
import twitter
from dateutil.parser import parse
from configparser import ConfigParser
from pypump import PyPump
from pypump import Client
from pypump.exceptions import ClientException
from requests.exceptions import ConnectionError

def simple_verifier(url):
	print('Please follow the instructions at the following URL:')
	print(url)
	return raw_input("Verifier: ") # the verifier is a string

class PumpTweetParser:
	"""Parses the ini file and provides the results on demand."""

	# This file must exist in the current directory.
	filename = 'PumpTweet.ini'

	# Parses the ini file.
	def parse_ini(self):
		print('Reading the config file...')

		# This verifies that the ini file exists.
		if not os.path.isfile(self.filename):
			message = self.filename + ' not found.'
			raise Exception(message)

		parser = ConfigParser()
		parser.read(self.filename)
		self._parser = parser
		self._history = True

		#self._recent = parser.get('history', 'recent')
		if 'recent' in parser['history']:
			self._recent = parser['history']['recent']
		else:
			self._history = False

		# Converts the date to a usable form.
		if 'published' in parser['history']:
			date = parser['history']['published']

			try:
				self._published = parse(date)
			except ValueError:
				pass
		else:
			self._history = False

	# Logs in to the Pump server.
	def pump_login(self):
		print('Logging into the Pump server...')

		username = self._parser.get('pump', 'username')

		client = Client(
			webfinger = username,
			name = "Pump.io",
			type = "native")

		try:
			pump = PyPump(
				client = client,
				verifier_callback = simple_verifier)
		except ConnectionError as e:
			domain = username.split('@')[1]	
			print('Error: Unable to connect to ' + domain + '.')
			print(e)
			sys.exit()
		except ClientException:
			domain = username.split('@')[1]	
			print('Error: Pump server not found at ' + domain + '.')
			sys.exit()

		me = pump.Person(username)
		
		self._username = username
		self._pump = pump
		self._me = me

	# Logs in to Twitter.
	def twitter_login(self):
		print('Logging into Twitter...')
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
		self._parser.set('history', 'recent', str(latest))
		self._parser.set('history', 'published', str(published))

		with open(self.filename, 'w') as inifile:
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
