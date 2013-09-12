from HTMLParser import HTMLParser

# Class for stripping HTML from text.
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

# Strips tags from HTML, returning regular text.
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
