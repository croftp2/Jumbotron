#!/usr/bin/env python

#Paul Croft
#February 5, 2018

import httplib
from sqlite3 import connect
from pprint import pformat, pprint
import xml.etree.ElementTree as ET


conn = connect("rss_database.db")
c = conn.cursor()

def add_podcast(inlink):
    site, reqstr = inlink.split('/',3)[2:]
    site, port = site.split(':')
#    print "site:port", site, port
    httpconn = httplib.HTTPConnection(site, port=port)
    httpconn.request("GET", '/' + reqstr)
    resp = httpconn.getresponse()
    tree = ET.parse(resp)
    conn.close()
    treeroot = tree.getroot()
    channel = treeroot.find("channel")
    for episode in channel.findall("item"):
#        print episode.find("title").text
        pass
    print "Title", channel.find("title").text
    print "Image", channel.find("image").find("url").text
    print "Link", channel.find("link").text

    return 1

def main():
    c.execute("DROP TABLE IF EXISTS podcasts")
    c.execute("DROP TABLE IF EXISTS episodes")

    c.execute("CREATE TABLE podcasts (title TEXT, image TEXT, link TEXT)")
    c.execute("CREATE TABLE episodes (title TEXT, description TEXT, pubdate TEXT, author TEXT, duration INT, episode_num INT, datalink TEXT, podcast_id INT)")


if __name__ == '__main__':
    exit(main())