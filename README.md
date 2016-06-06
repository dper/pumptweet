PumpTweet
=========

A Python script that cross posts from a Pump.io server to Twitter.


Overview
========

If you aren't familiar with [pump.io](http://pump.io/), take a look at <https://microca.st/>.  Try it out and see what you think!  This script is for people already using a pump.io service (like microca.st, but there are many others, and you can run your own).

There are many different kinds of activities.  Here, we look for *notes*, which are like regular blog entries.  We find a note, shorten it, make a URL to the original, and tweet it.  In other words, we're cross-posting from pump.io to Twitter.

When you compose a note, you choose the recipients.  This script will cross-post your note if it's `To: Public` or `CC: Public`.  Posts that aren't sent to `Public` are ignored.  Other pump activities (comments, likes, etc.) are excluded.  It's not obvious how they would be of interest on Twitter.

This program is designed to be run as a cron job on a regular basis.


Example
=======

Pump notes can be of any length, but tweets are limited to 140 characters.  This program crops notes either (1) at the first line break or (2) as close as it can to 140 characters while still leaving room for a link to the original note.  Here are some examples.

Example pump #1.

    Have a great weekend, everyone!

Example tweet #1. The URL is a link to the original note.

    Have a great weekend, everyone! http://ur1.ca/fislx
    
Example pump #2.

    I have a technical question about cooling fans.
    
    My processor on my new machine is an i7. I'm using a SilverStone AR-01 heat sink. The heat sink is...

Example tweet #2. Only the first line of the note is retained.

    I have a technical question about cooling fans.… http://ur1.ca/fihk8


Contact
=======

If you want to contact the author, here are some ways.  Bug reports and improvements are always welcome.

* <https://microca.st/dper>
* <https://twitter.com/dpp0>
* <https://dperkins.org/tag/contact.html>


PyPI Installation
=================

To start with, you need Python.  Python 3.4 and 3.5 have been tested and work.  Older versions probably don't.

It is easiest to install from [PyPI](https://pypi.python.org/pypi/pumptweet).  First, make a `virtualenv`.  The `virtualenv` is nice because it means software you install here won't interfere with anything else on the system.  Also, if you find something is wrong or you're otherwise unhappy, you can delete the `pumptweet` directory.

    $ cd
    $ mkdir pumptweet
    $ virtualenv pumptweet
    $ cd pumptweet
    $ source bin/activate
    (pumptweet)$ pip install pumptweet

Assuming no errors showed up, you've installed `pumptweet`.  The next step is to configure it.


Source Installation
===================

* Browse: <https://dperkins.org/git/gitlist/pumptweet.git>.
* Clone: <https://dperkins.org/git/public/pumptweet.git>.
* GitHub: <https://github.com/dper/pumptweet.git>.

If you want to make custom modifications, consider a `git` install.  These instructions are for a Debian system.  Other Linux and Unix distributions should be similar.  First, get the source code and put it in a `virtualenv`.

    $ cd
    $ git clone https://github.com/dper/pumptweet
    $ virtualenv pumptweet
    $ cd pumptweet
    $ source bin/activate

The command prompt should now begin with `(pumptweet)`.  You may also need to install some dependencies, including [PyPump](https://github.com/xray7224/PyPump) and [python-twitter](https://github.com/bear/python-twitter).

    (pumptweet)$ pip3 install pypump
    (pumptweet)$ pip3 install python-twitter


Configuration
=============

In order to use the script, create a file called `PumpTweet.ini` that looks something like this.

    [pump]
    username = 
    
    [twitter]
    key = 
    secret = 
    token = 
    token_secret = 
    
    [history]
    recent = 
    published = 

All of the values in `[pump]` and `[twitter]` must be filled in, but the two entries in `[history]` can be left blank.  If you fail to fill in the top two sections, you'll get some kind of error when running the script.  For convenience, a file called `PumpTweet.ini.blank` is included.  Copy that file or the above text to `PumpTweet.ini` and fill in the necessary sections.

Place the `PumpTweet.ini` filein the base installation directory.  For example, I installed pumptweet into `~/pumptweet` earlier in this document.  My configuration file should be located at `~/pumptweet/PumpTweet.ini`.


Configuring Pump
================

The script uses [PyPump](https://pypump.readthedocs.org/en/latest/gettingstarted/qnd.html) to communicate with pump servers. This assumes you already have a pump account.

The first thing you need to do is put your username (which looks like an email address) into the `[pump]` section of the ini file. Next, run:

    $ cd pumptweet
    $ source bin/activate
    (pumptweet)$ ./pt.py

At this point, you'll get a hyperlink to your pump server. Paste the link into your browser to open a page where you can sign in and give the application the necessary permissions. Paste the verifier back into the prompt to continue. This is all you need to do for `[pump]`.


Configuring Twitter
===================

To get the client validated with Twitter, use your favorite web browser.  This assumes you already have a Twitter account.

* Go to <https://apps.twitter.com/> and sign in.
* Click `Create new app`.
* You need to give it a name (like `pumptweet314`), a description (like `A cross-posting script from Pump to Twitter.`), and a website (if you make a fork of pumptweet on GitHub, that would be a nice URL, but anything is OK).  Also check the box agreeing with their terms and answer the CAPTCHA.
* Click on the `Settings` tab.  Change `Access` to `Read and Write`.  At the bottom of the screen, click `Update this Twitter application's settings`.
* Click on the `Details` tab. Near the bottom of the screen click `Create my access token`.
* Click on the `Keys and Access Tokens` tab.  This screen should show you the four values needed in the ini file.  Copy and paste them.  That's all you need to do for `[twitter]`.


Running the script
==================

To run the script, just call it.  If you're missing any dependencies (like the ones documented above), you'll find out about it here.  If you installed pumptweet from source, run it as follows.

    (pumptweet)$ ./pt.py

If you installed it using `pip`, run it as follows.

    (pumptweet)$ ./bin/pt.py

If everything is working, you should see something like the following.  In this example, there's one new note and therefore one new tweet which is posted to Twitter.

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

If you run the script a second time, it looks to see if there is anything new since last time it ran.  In the below example, it looks at one post and stops, because that post isn't any newer than what the script handled last time around.  Nothing is posted to Twitter.

    Reading the config file...
    Logging into the pump.io server...
    Logging into Twitter...
    Converting posts to tweets...
    Looking at pump.io outbox activity...
    > note (2013-09-12 11:31:49+00:00)
    Printing tweets...
    Posting to Twitter...
    Updating history...

For convenience, there is a bash script, `pt.sh` that does `virtualenv` stuff for you.  Call that script from the command line to make sure it works.  If you installed from source, run it as follows.

    $ cd /home/me/pumptweet && pt.sh

If you installed using `pip`, run it as follows.

    $ cd /home/me/pumptweet && ./bin/pt.sh


Cron and rate limits
====================

Suppose you have installed the program in `/home/me/pumptweet` and have tested it using `pt.sh` to confirm that all is in working order.  The next thing to do is to make a cron job (using `crontab -e`) like the following.  The following cron job runs every five minutes.

    */5 * * * * cd /home/me/pumptweet && ./pt.sh > /dev/null

For most users, there is no worry, but if you tend to write many notes in a short amount of time, cross posting can be somewhat delicate.  Twitter has a rate limit, though I don't know exactly what it is.  This script posts up to three tweets at a time.  If you have written five notes since the last time you called it, the newest three will become tweets and the oldest two will be forgotten.

If you find that you write many notes and they're being skipped, you can change `PumpTweet.py` and post more than three at a time.  But don't raise the value too high, or you might hit the Twitter rate limit, start looking spammy to your Twitter followers, or both.  A better approach might be a more frequent cron job.


Errors
======

Identifying errors can be difficult.  If the Pump or Twitter servers are completely offline, you will get an obvious error message, but if they're partly offline, you might not.  Similarly, if your login is incorrect, you might see confusing error messages.  If you're not sure what's going wrong, you are encouraged to open an issue, contact the developers, or post a message to the Pump network.


Testing
=======

If you're trying to modify the script or track down some other error, you might want to do test runs.  In that case, call the script as follows, updating the directories according to where you installed it.

    (pumptweet) $ pt.py --test

For the (very short) command line help documentation, use this command.

    (pumptweet) $ pt.py --help


GNU social
==========

[GNU social](http://gnu.io/social/) has a Twitter-like API, and you can use this script, with a few modifications, to cross-post from Pump.io to GNU social.  [@sazius](https://pump.saz.im/sazius/note/jdTJx2pQRGiEDpB5eDlXEg) has done so, and here is what he says.

> It was quite easy: just add the parameter `base_url='https://your.gnu.social/api'` to the call to `twitter.API()` in `twitter_login` in `PumpLogin.py`. I guess you could have that as a configurable parameter.
>
> Next problem was to get the OAuth token from GNU Social, I used the `get_access_token.py` script, but you have to add `?oauth_callback=oob` to the `REQUEST_TOKEN_URL`, and of course replace the Twitter API URLs with the one for GNU social.


Thanks
======

The `pump.io` community at large has helped advertise this project.  Thanks to everyone there for support.  See `AUTHORS.md` for a list of those wonderful individuals who contributed code.  
