#!/usr/bin/env python

#Paul Croft
#February 5, 2018

import urllib
from sqlite3 import connect
from pprint import pformat, pprint
import xml.etree.ElementTree as ET


conn = connect("rss_database.db")
c = conn.cursor()

def get_podcasts():
    retval = []
    podcasts = c.execute("SELECT title, image, link FROM podcasts").fetchall()
    for t,i,l in podcasts:
        podcast_episodes = []
        for et, el, ea, ed, ep, eg in c.execute("SELECT title, link, audio_type, description, pubdate, guid FROM episodes WHERE podcast_id == (SELECT rowid FROM podcasts WHERE link == ?)", (l, )).fetchall():
            podcast_episodes.append({ \
                "title":et, \
                "link":el, \
                "audio_type":ea, \
                "description":ed, \
                "pubDate":ep, \
                "guid":eg, \
                })
        retval.append({"title":t,"image_link":i,"link":l, "episodes": podcast_episodes})
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
    site, port = site.split(':')
    tree = ET.parse(urllib.urlopen(inlink))
    treeroot = tree.getroot()
    channel = treeroot.find("channel")


    title = channel.find("title").text
    image_link = "NULL"
    link = channel.find("link").text

    title = str(title)#XML is just so wonderful
    image_link = str(image_link)
    link = str(link)

    # print "HERE", repr(title), repr(image_link), repr(link)
    c.execute("INSERT INTO podcasts VALUES (?,?,?)",(title, image_link, link, ))

    podcast_rowid = c.execute("SELECT rowid FROM podcasts WHERE link == ?", (link, )).fetchone()[0]
    c.executemany("INSERT INTO episodes VALUES (?,?,?,?,?,?,{})".format(podcast_rowid), map(episode_extrator, channel.findall("item")))
    return 1

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


if __name__ == '__main__':
    exit(main())