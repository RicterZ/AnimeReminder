# -*- coding:utf-8 -*-
import web
import re, os

import json
import urllib,urllib2
import random, hashlib, string
import zipfile, datetime
import jinja2 as jj

from lib.anime import AnimeDataGetter
from lib.error import *

web.config.debug = False
#web.header('Content-type', "text/html; charset=utf-8")
tempdir = 'templates/'
env = jj.Environment(loader = jj.FileSystemLoader(tempdir))

db = web.database(
    host = 'us1.rpvhost.net',
    dbn  = 'mysql',
    db   = '', 
    user = '', 
    pw   = ''
)
