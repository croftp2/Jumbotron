#!/usr/bin/env python

#Paul Croft
#February 5, 2018

from bottle import get, post, static_file, template, run, request, response

from argparse import ArgumentParser
import os
from pprint import pformat, pprint
from sqlite3 import OperationalError, IntegrityError

import db_utils

@get("/episodes/<episode_id>")
def get_episode_html(episode_id):
    data = db_utils.get_episode_info(episode_id)
    return template("templates/episode_chunk.html", edata=data)

@get("/podcasts/<podcast_id>")
def get_podcast_page(podcast_id):
    podcast_title = db_utils.get_podcast_title(podcast_id)
    episodes = db_utils.get_episodes(podcast_id)
    return template("templates/podcast_page.html", episodes=episodes, podcast_title=podcast_title)

@post("/new_rss/")
def api_add_podcast():
    post_data = request.body.read(1024)
    try:
        title = db_utils.add_podcast(post_data)
        return title
    except ValueError:
        response.status = 406
        return "misc failed"
    except IntegrityError:
        response.status = 409
        return "duplicated podcast"


@get("/podcasts_html/")
def get_podcasts_html():
    podcasts = db_utils.get_podcasts()
    return template("templates/podcasts.html", podcasts=podcasts)


@get("/")
def index():
    # podcasts = db_utils.get_podcasts()
    # return template("templates/main.html", podcasts=podcasts)
    return template("templates/main.html")

@get("/css/<cssfile>")
def cssfile(cssfile):
    return static_file(cssfile, root="css")

@get("/js/<jsfile>")
def jsfile(jsfile):
    return static_file(jsfile, root="js")

def main():

    try:
        print("{} podcasts tracked".format(db_utils.get_number_of_podcasts()))
    except OperationalError:
        print("No tables. Building tables now...")
        db_utils.build_tables()
        print("Done")

    try:
        run(host="0.0.0.0", port=os.environ["PORT"])
    except KeyError:
        run(host="0.0.0.0", port=14233)

if __name__ == '__main__':
    exit(main())

