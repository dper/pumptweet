PumpTweet
=========

A Python script that cross posts from a Pump.io server to Twitter.

Overview
========

If you aren't familiar with Pump.io, take a look at <https://microca.st/>.  Try it out and see what you think!  This script is for people already using a Pump.io service (like Microca.st, but there are many others, and you can run your own).

On Pump.io (<http://pump.io/>), there are many different kinds of activities.  Here, we only look for *notes*, which are essentially regular blog entries.  We find notes on Pump.io, shorten them, make a URL to the original note (very useful if it's a long note), and post the short version as a tweet on Twitter.

Other Pump.io activities (such as comments, likes, dislikes, and following new people) are excluded from here, because it's not obvious at face value what, if anything, among them would be of interest to a reader on Twitter.

This program is designed to be run as a cron job on a regular basis (for example, every 30 or 60 minutes).

There are other programs that do similar things (for example, <http://brdcst.it/>).  If you enjoy using them, by all means continue!  On the other hand, if this script is more to your needs, wonderful.  If you browse the source code, you'll notice that (a) it's really short, because all the hard work was done by the wonderful people who wrote the dependencies, and (b) it's simple, so you can make changes if you like.

Issues
======

If you see any issues, obvious but missing features, or problems with the documentation, feel free to open an issue at <https://github.com/dper/PumpTweet/issues>.

Installation
============

This documents how to install PumpTweet on Debian.  Other Linux distributions should be nearly identical.

This installs the script in `~/src/PumpTweet`.  First, get the code from GitHub (<https://github.com/dper/PumpTweet>).

    $ git clone https://github.com/dper/PumpTweet
    $ cd PumpTweet

There are several choices for dependencies.  You can install them globally or simply place everything here in a `virtualenv`.  The simplest choice is using `virtualenv`.  It's nice because all the dependencies will be placed inside this one directory, and if you decide things are causing problems, you can just delete the entire directory without affecting anything else.

    $ virtualenv PumpTweet

Go into the directory and enable `virtualenv`.

    $ cd PumpTweet
    $ source bin/activate

The command prompt should now begin with `(PumpTweet)`.

You may also need to install some dependencies like PyPump (<https://github.com/xray7224/PyPump>), python-twitter (<https://github.com/bear/python-twitter>), and BeautifulSoup (<http://www.crummy.com/software/BeautifulSoup/>).

    $ pip install pypump
    $ pip install python-twitter
    $ pip install BeautifulSoup

Configuration
=============

In order to use the script, you need to create a file called `PumpTweet.ini` that looks something like this.

    [pump]
    username = 
    key = 
    secret = 
    token = 
    token_secret = 
    
    [twitter]
    key = 
    secret = 
    token = 
    token_secret = 
        
    [history]
    recent = 
    published = 

All of the values in `[pump]` and `[twitter]` must be filled in, but `[history]` can be left blank.

Running the script
==================

To run the script, just call it.  If you're missing any dependencies (like the ones documented above), you'll find out about it here.

    $ python PumpTweet.py

If everything is working correctly, output should look like the following.  In this example, there's one new note and therefore one new tweet.

    Reading the config file...
    Logging into the pump.io server...
    Logging into Twitter...
    Converting posts to tweets...
    Looking at pump.io outbox activity...
    > note (2013-09-12 11:31:49+00:00)
    > note (2013-09-12 10:40:24+00:00)
    Printing tweets...
    > Microca.st: Someone put on a pot of coffee at 3PM today. I can't have coffee in the afternoon and reliably get to ... http://ur1.ca/fhy3z
    Posting to Twitter...
    Updating history...

If you run the script a second time, it looks to see if there is anything new since last time it ran.  In the below example, it looks at one post and stops, because that post isn't any newer than what the script handled last time around.

    Reading the config file...
    Logging into the pump.io server...
    Logging into Twitter...
    Converting posts to tweets...
    Looking at pump.io outbox activity...
    > note (2013-09-12 11:31:49+00:00)
    Printing tweets...
    Posting to Twitter...
    Updating history...
