# -*- coding:utf-8 -*-
import web
import re, os

import json
import jinja2 as jj
import urllib,urllib2
import random, hashlib, string
import zipfile, datetime

from lib.anime import AnimeDataGetter
from lib.error import *

web.config.debug = False
env = jj.Environment(loader = jj.FileSystemLoader('templates'))

db = web.database(
    host = 'faceair.net',
    dbn  = 'mysql',
    db   = 'ricter_newanime', 
    user = 'ricter', 
    pw   = 'Canyue123'
)
