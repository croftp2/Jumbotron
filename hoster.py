#!/usr/bin/env python

#Paul Croft
#February 5, 2018

from bottle import get, static_file, template, run

from pprint import pformat, pprint

@get("/")
def index():
    return template("templates/main.html")

def main():
    return 0

if __name__ == '__main__':
    exit(main())

