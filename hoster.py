#!/usr/bin/env python

#Paul Croft
#February 5, 2018

from bottle import get, post, static_file, template, run, request

from pprint import pformat, pprint

import db_utils

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

def main():

    db_utils.add_podcast("http://localhost:1233/replyall.xml")
    db_utils.add_podcast("http://localhost:1233/serial.xml")
    run(host="0.0.0.0",port=14233)

if __name__ == '__main__':
    exit(main())

