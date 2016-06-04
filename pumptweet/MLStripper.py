# coding=utf-8

from html.parser import HTMLParser
import html

# Class for stripping HTML from text.
class MLStripper(HTMLParser):

	def __init__(self):
		super().__init__(convert_charrefs=True)
		self.reset()
		self.fed = []

	def handle_data(self, d):
		self.fed.append(d)

	def handle_starttag(self, tag, attrs):
		if tag == 'br':
			self.fed.append("\n")

	def handle_endtag(self, tag):
		if tag == 'p':
			self.fed.append("\n")

	def get_data(self):
		return ''.join(self.fed)

# Replaces HTML entities with actual characters.
def replace_entities(html):
	unifiable = [
		('&amp;', '&'), 
		('&nbsp;', ' '),
		('&#39;', "'"),
		('&quot;', "'"),
		('&ndash;', '-'),
		('&mdash;', u'–'),
		('&rarr;', u'→'),
		('&larr;', u'←'),
		('&lrarr;', u'↔'),
		('&ldquo;', '"'),
		('&rdquo;', '"'),
	]

	for (entity, char) in unifiable:
		html = html.replace(entity, char)

	return html

# Strips tags from HTML, returning regular text.
def strip_tags(text):
	text = replace_entities(text)

	# Converts HTML characters back to unicode.
	# This keeps them from being stripped later.
	text = html.unescape(text)

	s = MLStripper()
	s.feed(text)
	return s.get_data()
