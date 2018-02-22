#!/usr/bin/env python

#Paul Croft
#February 5, 2018

from operator import itemgetter
import urllib
from sqlite3 import connect
import string
from sys import argv
from pprint import pformat, pprint
import xml.etree.ElementTree as ET

#because xml is the worst!
XMLNAMESPACES = {"itunes":"http://www.itunes.com/dtds/podcast-1.0.dtd"}

conn = connect("rss_database.db")
c = conn.cursor()

class Episode(object):
    def __init__(self, ineid):
        edata = c.execute("""
SELECT 
    episodes.rowid, 
    episodes.title,
    episodes.link,
    episodes.audio_type,
    episodes.description,
    episodes.pubdate,
    episodes.guid,
    podcasts.title,
    podcasts.image
FROM episodes
JOIN podcasts ON
    episodes.podcast_id == podcasts.rowid
WHERE episodes.rowid == ?
LIMIT 1
""", (ineid, )).fetchone()

        self.eid = edata[0]
        self.title = edata[1],
        self.link = edata[2],
        self.audio_type = edata[3],
        self.description = edata[4],
        self.pubdate = edata[5],
        self.guid = edata[6],
        self.podcast_title = edata[7],
        self.podcast_image = edata[8],

    def __repr__(self):
        return "<Episode {}>".format(self.eid)


def get_episode_info(ineid):
    return Episode(ineid)

def get_episodes(inpid):
    erowids = c.execute("SELECT rowid FROM episodes WHERE podcast_id == ?",(inpid, )).fetchall()
    episodes = map(Episode, map(itemgetter(0), erowids))
    return episodes


def get_podcasts():
    retval = []
    podcasts = c.execute("SELECT rowid, title, image, link FROM podcasts ORDER BY TITLE").fetchall()
    for r,t,i,l in podcasts:
        retval.append({"pid":r, "title":t,"image_link":i,"link":l})
    return retval

def episode_extrator(inepisode):

    #TODO this could all be better
    temp = [ \
        inepisode.find("title"), \
        inepisode.find("enclosure").attrib["url"], \
        inepisode.find("enclosure").attrib["type"], \
        inepisode.find("description"), \
        inepisode.find("pubDate"), \
        inepisode.find("guid"), \
        ]
    for i in xrange(len(temp)):
        if temp[i] is not None and type(temp[i]) is not str:
            temp[i] = temp[i].text
    return temp

def add_podcast(inlink):
    site, reqstr = inlink.split('/',3)[2:]
    port = 80
    if ':' in site:
        site, port = site.split(':')
    tree = ET.parse(urllib.urlopen(inlink))
    treeroot = tree.getroot()
    channel = treeroot.find("channel")


    title = channel.find("title").text
    image_link = channel.find("itunes:image", XMLNAMESPACES).attrib["href"]
    link = channel.find("link").text

    title = str(title)#XML is just so wonderful
    image_link = str(image_link)
    link = str(link)

    # print "HERE", repr(title), repr(image_link), repr(link)
    c.execute("INSERT INTO podcasts VALUES (?,?,?)",(title, image_link, link, ))

    podcast_rowid = c.execute("SELECT rowid FROM podcasts WHERE link == ?", (link, )).fetchone()[0]
    c.executemany("INSERT INTO episodes VALUES (?,?,?,?,?,?,{})".format(podcast_rowid), map(episode_extrator, channel.findall("item")))
    return 1

def get_podcast_title(inpid):
    return c.execute("SELECT title FROM podcasts WHERE rowid == ? LIMIT 1", (inpid,)).fetchone()[0]

def main():
    c.execute("DROP TABLE IF EXISTS podcasts")
    c.execute("DROP TABLE IF EXISTS episodes")

    c.execute("CREATE TABLE podcasts (title TEXT, image TEXT, link TEXT UNIQUE)")
    c.execute("""
CREATE TABLE episodes (
    title TEXT, 
    link TEXT,
    audio_type TEXT,
    description TEXT, 
    pubdate TEXT, 
    guid TEXT,
    podcast_id INT)""")

    podcast_list = open(argv[1]).read().split('\n')
    podcast_list = filter(None, map(string.strip, podcast_list))#Remove blank lines
    podcast_list = filter(lambda x:"#" != x[0],podcast_list)#Remove commented items
    podcast_list = set(podcast_list)#Remove duplicates

    for podcast in podcast_list:
        add_podcast(podcast)

    conn.commit()

if __name__ == '__main__':
    exit(main())