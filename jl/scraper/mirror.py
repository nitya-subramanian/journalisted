#!/usr/bin/env python2.4
#
# Copyright (c) 2007 Media Standards Trust
# Licensed under the Affero General Public License
# (http://www.affero.org/oagpl.html)
#
# Scraper for Mirror and Sunday Mirror
#
# TODO: see how the sunday mirror is handled, wrt RSS feeds!

import re
from datetime import datetime
import time
import string
import sys
import urlparse

import site
site.addsitedir("../pylib")
from BeautifulSoup import BeautifulSoup
from JL import ukmedia, ScraperUtils



def FindRSSFeeds():
    """ fetch a list of RSS feeds for the mirror.

    returns a list of (name, url) tuples, one for each feed
    """

    # miriam blacklisted for now, as her column is redirected to blogs (and picked up by our blog rss list)
    url_blacklist = ( '/fun-games/', '/pictures/', '/video/', '/miriam/' )

    ukmedia.DBUG2( "Fetching list of rss feeds\n" );

    sitemap_url = 'http://www.mirror.co.uk/sitemap/'
    html = ukmedia.FetchURL( sitemap_url )
    soup = BeautifulSoup(html)

    feeds = []
    for a in soup.findAll( 'a', {'class':'sitemap-rss' } ):
        url = a['href']
#        a2 = a.findNextSibling( 'a' )
#        if a2:
#            title = a2.renderContents( None )
#        else:
        m = re.search( r'mirror.co.uk/(.*)/rss[.]xml', url )
        title = m.group(1)

        skip = False
        for banned in url_blacklist:
            if banned in url:
                ukmedia.DBUG2( " ignore feed '%s' [%s]\n" % (title,url) )
                skip = True

#        print "%s: %s" %(title,url)
        if not skip:
            feeds.append( (title,url) )

    return feeds


# feedburner blogs, see "http://www.mirror.co.uk/opinion/blogs/"
blog_rssfeeds = [
    ("blog: 3pm", "http://feeds.feedburner.com/mirror-3pm"),
    ("blog: Amber & friends", "http://feeds.feedburner.com/mirrorfashion"),
    ("blog: Big Brother'", "http://feeds.feedburner.com/big-brother/" ),
    # Christopher Hitchens rss link is borked
    #("blog: Christopher Hitchens", 'http://feeds.feedburner.com/.....'),
    ("blog: Cricket", "http://feeds.feedburner.com/mirror/cricket"),
    ("blog: Dear Miriam", "http://feeds.feedburner.com/dear-miriam"),
    ("blog: Football Spy", "http://feeds.feedburner.com/FootballSpy" ),
    ("blog: Kevin Maguire & Friends","http://feeds.feedburner.com/KevinMaguire" ),
    # tv blog handled by main site
#    ("blog: Kevin O'Sullivan", '' ),
    ("Mirror Investigates","http://feeds.feedburner.com/mirror/investigations" ),
    # science one is also borked...
#    ("Science, Health and the Environment", "http://feeds.feedburner.com/investigations" ),
    # jim shelly handled by main site
    #("Shelleyvision", "" ),
    ("Showbiz with Zoe", "http://feeds.feedburner.com/showbiz-with-zoe" ),
    # Sue Carroll handled by main site
#    ("Sue Carroll", "" ),
    ("The Sex Doctor", "http://feeds.feedburner.com/sex-doctor/" ),
]



OBSOLETE_mirror_rssfeeds = {
    # feed not on the mirror sitemap...
    "Kevin Maguire & Friends": "http://feeds.feedburner.com/KevinMaguire",
    # raw feedlist generated by hacks/mirror-scrape-rsslist

    "News": "http://www.mirror.co.uk/newsrss.xml",
    "Top Stories": "http://www.mirror.co.uk/newsrss.xml",
#   "Latest Pictures": "http://www.mirror.co.uk/news/newspix/rss.xml",
    "Columnists": "http://www.mirror.co.uk/news/columnists/rss.xml",
    "Front Pages": "http://www.mydailymirror.com/rss.xml",
    "Investigations": "http://www.mirror.co.uk/news/investigates/rss.xml",
#   "Jobs": "http://www.mirror.co.uk/news/jobs/rss.xml",
#   "Kevin Maguire's blog": "http://maguire.mirror.co.uk/rss.xml",
    "Money & Business": "http://www.mirror.co.uk/news/money/rss.xml",
    "Motoring": "http://www.mirror.co.uk/news/motoring/rss.xml",
    "Technology & Gaming": "http://www.mirror.co.uk/news/technology/rss.xml",
    "Travel": "http://www.mirror.co.uk/news/travel/rss.xml",
#   "Voice of the Mirror": "http://www.mirror.co.uk/news/voiceofthemirror/rss.xml",
#   "Weather": "http://www.mirror.co.uk/news/weather/rss.xml",
    "Weird World": "http://www.mirror.co.uk/news/weirdworld/rss.xml",
    "Sport": "http://www.mirror.co.uk/sport/rss.xml",
    "Top Sports News": "http://www.mirror.co.uk/sport/latest/rss.xml",
#   "Latest Pictures": "http://www.mirror.co.uk/sport/sportpix/rss.xml",
    "Football": "http://www.mirror.co.uk/sport/football/rss.xml",
    "Columnists": "http://www.mirror.co.uk/sport/columnists/rss.xml",
#   "Fantasy Football": "http://www.mirror.co.uk/sport/ytm/rss.xml",
    "Athletics": "http://www.mirror.co.uk/sport/athletics/rss.xml",
    "Boxing": "http://www.mirror.co.uk/sport/boxing/rss.xml",
    "Cricket": "http://www.mirror.co.uk/sport/cricket/rss.xml",
    "Darts": "http://www.mirror.co.uk/sport/darts/rss.xml",
    "Golf": "http://www.mirror.co.uk/sport/golf/rss.xml",
    "Motorsports": "http://www.mirror.co.uk/sport/motorsport/rss.xml",
    "Racing": "http://www.mirror.co.uk/sport/racing/rss.xml",
    "Rugby": "http://www.mirror.co.uk/sport/rugby/rss.xml",
    "Snooker": "http://www.mirror.co.uk/sport/snooker/rss.xml",
    "Tennis": "http://www.mirror.co.uk/sport/tennis/rss.xml",
    "Showbiz": "http://www.mirror.co.uk/showbiz/rss.xml",
    "Top Showbiz News": "http://www.mirror.co.uk/showbiz/latest/rss.xml",
#   "Latest Pictures": "http://www.mirror.co.uk/showbiz/showbizpix/rss.xml",
    "3am": "http://www.mirror.co.uk/showbiz/3am/rss.xml",
    "TV & Film": "http://www.mirror.co.uk/showbiz/tv/rss.xml",
    "TV Land": "http://www.mirror.co.uk/showbiz/tv/tvland/rss.xml",
#   "Filmstore": "http://www.mirror.co.uk/showbiz/filmstore/rss.xml",
    "The Ticket": "http://www.mirror.co.uk/showbiz/theticket/rss.xml",
    "Lifestyle": "http://www.mirror.co.uk/showbiz/yourlife/rss.xml",
#   "Dating": "http://www.mirror.co.uk/showbiz/dating/rss.xml",
    "Health": "http://www.mirror.co.uk/showbiz/yourlife/sexandhealth/rss.xml",
#   "Horoscopes": "http://www.mirror.co.uk/showbiz/horoscopes/rss.xml",
#   "Slimming Club": "http://www.mirror.co.uk/showbiz/slimming/rss.xml",
    "Your Life": "http://www.mirror.co.uk/showbiz/yourlife/rss.xml",
}

OBSOLETE_sundaymirror_rssfeeds = {
    "News": "http://www.sundaymirror.co.uk/news/rss.xml",
    "Sunday": "http://www.sundaymirror.co.uk/news/sunday/rss.xml",
    "Latest news": "http://www.sundaymirror.co.uk/news/dailynews/rss.xml",
    "Columnists": "http://www.sundaymirror.co.uk/news/columnists/rss.xml",
    "Your Money": "http://www.sundaymirror.co.uk/news/yourmoney/rss.xml",
    "Motoring": "http://www.sundaymirror.co.uk/news/motoring/rss.xml",
    "Homes & Holidays": "http://www.sundaymirror.co.uk/news/homesandholidays/rss.xml",
#   "Weather": "http://www.sundaymirror.co.uk/news/weather/rss.xml",
    "Sport": "http://www.sundaymirror.co.uk/sport/rss.xml",
    "Latest Sport": "http://www.sundaymirror.co.uk/sport/latestsport/rss.xml",
    "Columnists": "http://www.sundaymirror.co.uk/sport/columnists/rss.xml",
    "Football": "http://www.sundaymirror.co.uk/sport/football/rss.xml",
    "Cricket": "http://www.sundaymirror.co.uk/sport/cricket/rss.xml",
    "Rugby": "http://www.sundaymirror.co.uk/sport/rugby/rss.xml",
    "Golf": "http://www.sundaymirror.co.uk/sport/golf/rss.xml",
    "Tennis": "http://www.sundaymirror.co.uk/sport/tennis/rss.xml",
    "Motorsport": "http://www.sundaymirror.co.uk/sport/motorsport/rss.xml",
    "Boxing": "http://www.sundaymirror.co.uk/sport/boxing/rss.xml",
    "Snooker": "http://www.sundaymirror.co.uk/sport/snooker/rss.xml",
    "Racing": "http://www.sundaymirror.co.uk/sport/racing/rss.xml",
    "Poker": "http://www.sundaymirror.co.uk/sport/poker/rss.xml",
#   "Casino": "http://www.sundaymirror.co.uk/sport/casino/rss.xml",
    "Showbiz": "http://www.sundaymirror.co.uk/showbiz/rss.xml",
    "Showbiz with Zoe": "http://www.sundaymirror.co.uk/showbiz/showbiznews/rss.xml",
    "Celebs On Sunday": "http://www.sundaymirror.co.uk/showbiz/celebsonsunday/rss.xml",
    "TV": "http://www.sundaymirror.co.uk/showbiz/tv/rss.xml",
    "Movies": "http://www.sundaymirror.co.uk/showbiz/movies/rss.xml",
    "Music": "http://www.sundaymirror.co.uk/showbiz/music/rss.xml",
    "Health": "http://www.sundaymirror.co.uk/showbiz/health/rss.xml",
#   "Horoscopes": "http://www.sundaymirror.co.uk/showbiz/horoscopes/rss.xml",
#   "Bingo": "http://www.sundaymirror.co.uk/showbiz/bingo/rss.xml",
#   "Dating": "http://www.sundaymirror.co.uk/showbiz/dating/rss.xml",
#   "Slimming": "http://www.sundaymirror.co.uk/showbiz/slimming/rss.xml",
}










def Extract( html, context ):
    url = context['srcurl']
    
    if re.search( r'/(blogs|fashion)[.]mirror[.]co[.]uk/', url ):
        return Extract_Blog( html, context )
    else:
        return Extract_MainSite( html, context )


def Extract_MainSite( html, context ):
    art = context
    soup = BeautifulSoup( html )


    if '/sunday-mirror/' in art['srcurl']:
        art['srcorgname'] = u'sundaymirror'
    else:
        art['srcorgname'] = u'mirror'

    maindiv = soup.find( 'div', { 'id': 'three-col' } )
    h1 = maindiv.h1

    title = h1.renderContents(None)
    title = ukmedia.FromHTMLOneLine( title )
    art['title'] = title

    # eg "By Jeremy Armstrong 24/07/2008"
    bylinepara = maindiv.find( 'p', {'class': 'article-date' } )
    bylinetxt = bylinepara.renderContents( None )
    bylinetxt = ukmedia.FromHTMLOneLine( bylinetxt )
    bylinepat = re.compile( r'\s*(.*?)\s*(\d{1,2}/\d{1,2}/\d{4})\s*' )
    m = bylinepat.match( bylinetxt )
    art['byline'] = m.group(1)
    art['pubdate'] = ukmedia.ParseDateTime( m.group(2) )

    # sometimes, only sundaymirror.co.uk in byline is only indicator
    if u'sundaymirror' in art['byline'].lower():
        art['srcorgname'] = u'sundaymirror'

    # if there was a gallery, pull out all the text we can before it gets culled
    galdiv = maindiv.find( 'div', {'class': re.compile('m-image_gallery')} )
    galtxt = u''
    if galdiv:
       for e in galdiv.findAll( re.compile( '^(h.|p)$' ) ):
            galtxt = galtxt + e.prettify( None )
    galtxt = ukmedia.SanitiseHTML( galtxt )

    # remove everything except for article text
    h1.extract()
    bylinepara.extract()
    # kill adverts, photos etc...
    for cruft in maindiv.findAll( 'div' ):
        cruft.extract()
    # sometimes a misplaced "link" element!
    for cruft in maindiv.findAll( 'link' ):
        cruft.extract()

    content = maindiv.renderContents(None)
    content = content + galtxt

    art['content'] = content
    art['description'] = ukmedia.FirstPara( content )

    if art['description'].strip() == u'':
        # check for obvious reasons we might get empty content
        t = art['title'].lower()
#        if re.search( r'\bpix\b', t ):
#            ukmedia.DBUG2("IGNORE pix page '%s' [%s]\n" % (art['title'],art['srcurl']) )
#            return None
        if re.search( r'^video:', t ):
            ukmedia.DBUG2("IGNORE video page '%s' [%s]\n" % (art['title'],art['srcurl']) )
            return None
        if re.search( r'\bdummy story\b', t ) or re.search( r'\bholding story\b', t ):
            ukmedia.DBUG2("IGNORE dummy story '%s' [%s]\n" % (art['title'],art['srcurl']) )
            return None

    return art





def Extract_Blog( html, context ):
    """extract article from a mirror.co.uk page"""

    art = context
    soup = BeautifulSoup( html )

    #maindiv = soup.find( 'div', { 'class': 'art-body' } )

    h1 = soup.find( 'h1', { 'class':'asset-name' } )
    art['title'] = ukmedia.FromHTML( h1.renderContents( None ) )

    body = soup.find( 'div', { 'class': 'asset-body' } )
    for cruft in body.findAll( 'span', {'class':re.compile("mt-enclosure")} ):
        cruft.extract()
    for cruft in body.findAll( 'img' ):
        cruft.extract()



    art['content'] = body.renderContents( None )
    #art['content'] = ukmedia.SanitiseHTML( art['content'] )

    art['description'] = ukmedia.FirstPara( art['content'] )

    # meta contains byline and date and permalink...
    # eg: "By Ann Gripper on Jul 21, 08 10:00 AM  in Golf"
    meta = soup.find( 'div', { 'class': 'asset-meta' } )
    metatxt = ukmedia.FromHTML( meta.renderContents( None ) )
    metatxt = u' '.join( metatxt.split() )
    metapat = re.compile( r"\s*(.*?)\s*on\s+(.*?(AM|PM))\s*" )
    m = metapat.search( metatxt )
    art['byline'] = m.group(1)
    art['pubdate'] = ukmedia.ParseDateTime( m.group(2) )

    return art




# to get unique id out of url
srcid_patterns = [


    # new-style:
    #  http://www.mirror.co.uk/news/top-stories/2008/07/24/exclusive-anne-darwin-vows-to-flee-to-panama-and-1million-fortune-when-out-of-jail-115875-20668758/
    # old-style (mirror):
    #  http://www.mirror.co.uk/news/topstories/2008/02/29/prince-harry-to-be-withdrawn-from-afghanistan-89520-20335665/
    # old-style (sunday mirror):
    #  http://www.sundaymirror.co.uk/news/sunday/2008/02/24/commons-speaker-michael-martin-in-new-expenses-scandal-98487-20329121/
    re.compile( "-([-0-9]+)(/([?].*)?)?$" ),

    # really old style:
    re.compile( "%26(objectid=[0-9]+)%26" ),

    # blogs:
    # http://blogs.mirror.co.uk/maguire/2008/07/beauty-and-the-beast.html
    # "http://fashion.mirror.co.uk/2008/04/sun-and-sandal.html"
    re.compile( "((blogs|fashion).mirror.co.uk/.*[.]html)" )
    ]

def CalcSrcID( url ):
    """ Calculate a unique srcid from a url """
    o = urlparse.urlparse( url )

    # only want pages from mirror.co.uk or sundaymirror.co.uk
    # domains (includes blogs.mirror.co.uk)
    if not o[1].endswith( 'mirror.co.uk' ) and not o[1].endswith('sundaymirror.co.uk'):
        return None

    for pat in srcid_patterns:
        m = pat.search( url )
        if m:
            break
    if not m:
        return None

    return 'mirror_' + m.group(1)


def ScrubFunc( context, entry ):
    title = context['title']
    title = ukmedia.DescapeHTML( title )
    title = ukmedia.UncapsTitle( title )    # all mirror headlines are caps. sigh.
    context['title'] = title

    url = context['srcurl']
    o = urlparse.urlparse( url )
    if o[1] == 'feeds.feedburner.com':
        # Luckily, feedburner feeds have a special entry
        # which contains the original link
        url = entry.feedburner_origlink
#        o = urlparse.urlparse( url )

#    if( 'blogs.mirror.co.uk' in context['srcurl'] ):
#        url = context['srcurl']
#    else:
#        # main mirror feeds go through mediafed.com. sigh.
#        # Luckily the guid has proper link (marked as non-permalink)
#        url = entry.guid

    # just in case they decide to change it...
    if url.find( 'mirror.co.uk' ) == -1:
        raise Exception, "URL not from mirror.co.uk or sundaymirror.co.uk ('%s')" % (url)

    if '/video/' in url:
        ukmedia.DBUG2( "ignore video '%s' [%s]\n" % (title,url) )


    context[ 'srcid' ] = CalcSrcID( url )
    context[ 'srcurl' ] = url
    context[ 'permalink'] = url

    return context




def ContextFromURL( url ):
    """Build up an article scrape context from a bare url."""
    context = {}
    context['srcurl'] = url
    context['permalink'] = url
    context[ 'srcid' ] = CalcSrcID( url )
    # looks like sundaymirror.co.uk domainname has been deprecated
    if 'sundaymirror.co.uk' in url or '/sunday-mirror/' in url:
        context['srcorgname'] = u'sundaymirror'
    else:
        context['srcorgname'] = u'mirror'

    context['lastseen'] = datetime.now()
    return context



def FindArticles():
    feeds = FindRSSFeeds()          # scrape the list of feeds for the main site
    feeds = feeds + blog_rssfeeds   # add the feedburner blogs
    found = ScraperUtils.FindArticlesFromRSS( feeds, u'mirror', ScrubFunc )
    return found



if __name__ == "__main__":
    ScraperUtils.RunMain( FindArticles, ContextFromURL, Extract )


