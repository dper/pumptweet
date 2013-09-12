#!/usr/bin/env python
#
#   shorturl.py
#   Shorts a long URL from command line, using ur1.ca.
#   Shows original page's title and short url.
#
#   ksaver, (at identi.ca); Sep, 2010.
#   version 0.2, Mar 2011.
#   Requires BeautifulSoup library in order to work properly:
#   http://www.crummy.com/software/BeautifulSoup/
#
#   Public Domain Code.

import sys
import urllib2

from BeautifulSoup import BeautifulSoup
from urllib  import urlencode

def shorten(longurl):
    shortener = 'http://ur1.ca/'
    urlparam = {'longurl': longurl}
    encparam = urlencode(urlparam)
    request  = urllib2.Request(shortener, encparam)
    htmlpage = urllib2.urlopen(request).read()
    htmlsoup = BeautifulSoup(htmlpage)
    txtmatch = htmlsoup.p.text.find('http')
    shorturl = htmlsoup.p.text[txtmatch:]
    return shorturl

def main(url):
    htmldoc = urllib2.urlopen(url).read()
    mysoup  = BeautifulSoup(htmldoc)
    title   = mysoup.title.text
    shorturl = shorten(url)
 
    print "'%s': %s\n" % (title, shorturl)
 
if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = raw_input("URL to short: ")
    main(url)
