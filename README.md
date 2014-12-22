PumpTweet
=========

A Python script that cross posts from a Pump.io server to Twitter.

Overview
========

If you aren't familiar with Pump.io (<http://pump.io/>), take a look at <https://microca.st/>.  Try it out and see what you think!  This script is for people already using a pump service (like microca.st, but there are many others, and you can run your own).

On Pump.io, there are many different kinds of activities.  Here, we only look for *notes*, which are essentially regular blog entries.  We find notes from our pump account, shorten them, make a URL to the original note (very useful if it's a long note), and post the short version as a tweet on Twitter.  In other words, we're cross-posting from Pump to Twitter.

When you compose a note, you choose the recipients.  This script will cross-post your note if it's `To: Public` or `CC: Public`.  Posts that aren't sent to `Public` are ignored.

Other pump activities (such as comments, likes, dislikes, and following new people) are excluded from this, because it's not obvious at face value what, if anything, among them would be of interest to a reader on Twitter.

This program is designed to be run as a cron job on a regular basis (for example, every five minutes).  The more frequent the cron job, the more up to date your cross posts are.

There are other programs that do similar things (for example, <http://brdcst.it/>).  If you enjoy using them, by all means continue to do so!  On the other hand, if this script fits your needs, wonderful.  If you browse the source code, you'll notice that (a) it's really short, because all the hard work was done by the wonderful people who wrote the dependencies, and (b) it's simple, so you can make changes if you like.

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

Issues
======

If you see any issues, obvious but missing features, or problems with the documentation, feel free to open an issue at <https://github.com/dper/PumpTweet/issues> or contact the author at <https://microca.st/dper>.

Installation
============

This documents how to install PumpTweet on Debian.  Other Linux distributions should be nearly identical.

This installs the script in `~/src/PumpTweet`.  First, get the code from GitHub (<https://github.com/dper/PumpTweet>).

    $ cd ~/src
    $ git clone https://github.com/dper/PumpTweet

There are several choices for dependencies.  You can install them globally or simply place everything here in a `virtualenv`.  The simplest choice is using `virtualenv`.  It's nice because all the dependencies will be placed inside this one directory, and if you decide things are causing problems, you can just delete the entire directory without affecting anything else.

    $ virtualenv PumpTweet

Go into the directory and enable `virtualenv`.

    $ cd PumpTweet
    $ source bin/activate

The command prompt should now begin with `(PumpTweet)`.

You may also need to install some dependencies like PyPump (<https://github.com/xray7224/PyPump>), python-twitter (<https://github.com/bear/python-twitter>), and BeautifulSoup (<http://www.crummy.com/software/BeautifulSoup/>).

    (PumpTweet)$ pip install pypump
    (PumpTweet)$ pip install python-twitter
    (PumpTweet)$ pip install BeautifulSoup

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

All of the values in `[pump]` and `[twitter]` must be filled in, but the two entries in `[history]` can be left blank.  If you fail to fill in the top two sections, you'll get some kind of error when running the script.  For convenience, a file called `PumpTweet.ini.blank` is included.  You can simply copy that file to `PumpTweet.ini` and fill in the necessary sections.

Configuring Pump
================

The script uses PyPump (<https://pypump.readthedocs.org/en/latest/gettingstarted/qnd.html>) to communicate with pump servers.  These instructions are based on the excellent PyPump documentation.  This assumes you already have a pump account.

    $ cd src/PumpTweet
    $ source bin/activate
    (PumpTweet)$ python
    
From the python prompt, do the following.
    
    from pypump import PyPump, Client
    
    def simple_verifier(url):
        print 'Please follow the instructions at the following URL:'
        print url
        return raw_input("Verifier: ") # the verifier is a string
        
    webfinger = "id@pump.server"
    name = "PumpTweet"
    type = "native"
    
    client = Client(webfinger=webfinger, name=name, type=type)
    pump = PyPump(client=client, verifier_callback=simple_verifier)
    
At this point, you'll get a hyperlink to your pump server.  Paste the link into your browser to open a page where you can sign in and give the application the necessary permissions.  Paste the verifier back into the Python prompt to continue.  Once you're signed in, you need to get the five values needed to automate this step in the future.  These should go in the `[pump]` section of the ini.

    >>> key = str(pump.get_registration()[0])
    >>> secret = str(pump.get_registration()[1])
    >>> token = str(pump.get_token()[0])
    >>> token_secret = str(pump.get_token()[1])

Copy and paste those four values into the ini file.  Your username is just your pump username, which looks like an email address.  This is all you need to do for `[pump]`. 

Configuring Twitter
===================

To get the client validated with Twitter, use your favorite web browser.  This assumes you already have a Twitter account.
* Go to <https://dev.twitter.com/>.
* Sign in using the link in the upper right corner.
* Hover your mouse over your avatar in the upper right corner. Click on `My applications`.
* Click `Create a new application`.
* You need to give it a name (like `PumpTweet314`), a description (like `A cross-posting script from Pump to Twitter.`), and a website (if you make a fork of PumpTweet on GitHub, that would be a nice URL, but anything is OK).  Also check the box agreeing with their terms and answer the CAPTCHA.
* Click on the `Settings` tab.  Change `Access` to `Read and Write`.  At the bottom of the screen, click `Update this Twitter application's settings`.
* Click on the `Details` tab. Near the bottom of the screen click `Create my access token`.
* Click on the `OAuth tool` tab.  This screen should show you the four values needed in the ini file.  Copy and paste them.  That's all you need to do for `[twitter]`.

Running the script
==================

To run the script, just call it.  If you're missing any dependencies (like the ones documented above), you'll find out about it here.

    (PumpTweet) $ python PumpTweet.py

If everything is working correctly, output should look like the following.  In this example, there's one new note and therefore one new tweet which is posted to Twitter.

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

For convenience, there is a Bash script, `PumpTweet.sh` that does `virtualenv` stuff for you.  Call that script from the command line to make sure it works.

    $ ./src/PumpTweet/PumpTweet.sh

Cron and rate limits
====================

Suppose you have installed the program in `/home/me/src/PumpTweet` and have tested it using `PumpTweet.sh` to confirm that all is in working order.  The next thing to do is to make a cron job (using `crontab -e`) like the following.  The following cron job runs every five minutes.

    */5 * * * * /home/me/src/PumpTweet/PumpTweet.sh > /dev/null

For most users, there is no worry, but if you tend to write many notes in a short amount of time, cross posting can be somewhat delicate.  Twitter has a rate limit, though I don't know exactly what it is.  This script is rather conservative and only posts up to three tweets at a time.  That means if you have written five pump notes since the last time you called this program, the newest three will become tweets and the oldest two will be entirely ignored.

If you find that you write many notes and they're being skipped, you can change the code in `PumpTweet.py` and post more than three at a time.  But don't raise the value too high, or you might hit the Twitter rate limit, start looking spammy to your Twitter followers, or both.  A better approach might be a more frequent cron job.

Testing
=======

If you're trying to modify the script or track down some other error, you might want to do test runs.  In that case, call the script as follows, updating the directories according to where you installed it.

    (PumpTweet) $ python PumpTweet.py --test

For the (very short) command line help documentation, use this command.

    (PumpTweet) $ python PumpTweet.py --help

GNU Social
==========

GNU social (http://gnu.io/social/) has a Twitter-like API, and you can use this script, with a few modifications, to cross-post from Pump.io to GNU social.  @sazius (<https://pump.saz.im/sazius/note/jdTJx2pQRGiEDpB5eDlXEg>) has done so, and here is what he says.

> It was quite easy: just add the parameter `base_url='https://your.gnu.social/api'` to the call to `twitter.API()` in `twitter_login` in `PumpLogin.py`. I guess you could have that as a configurable parameter.
>
> Next problem was to get the OAuth token from GNU Social, I used the `get_access_token.py` script, but you have to add `?oauth_callback=oob` to the `REQUEST_TOKEN_URL`, and of course replace the Twitter API URLs with the one for GNU social.

Thanks
======

The `pump.io` community at large has helped advertise this project.  Thanks to `diocles` for some bug reports and patches.  The code for filtering out non-public posts came from `sazius`, as did information on posting to GNU social.
