#!/usr/bin/env python

#Paul Croft
#February 5, 2018

from bottle import get, post, static_file, template, run, request

import os
from pprint import pformat, pprint

import db_utils

@get("/episodes/<episode_id>")
def get_episode_html(episode_id):
    data = db_utils.get_episode_info(episode_id)
    return template("templates/episode_chunk.html", edata=data)

@post("/newpodcast/")
def add_podcast():
    post_data = request.data
    print post_data
    return index

@get("/")
def index():
    podcasts = db_utils.get_podcasts()
#    pprint(podcasts)
    return template("templates/main.html", podcasts=podcasts)

@get("/css/<cssfile>")
def cssfile(cssfile):
    return static_file(cssfile, root="css")

@get("/js/<jsfile>")
def jsfile(jsfile):
    return static_file(jsfile, root="js")

def main():

    try:
        run(host="0.0.0.0",port=os.environ["PORT"])
    except KeyError:
        run(host="0.0.0.0",port=14233)

if __name__ == '__main__':
    exit(main())

