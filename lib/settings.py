# -*- coding:utf-8 -*-
import web
import re, os

import json
import urllib,urllib2
import random, hashlib, string
import zipfile, datetime

from lib.anime import AnimeDataGetter
from lib.error import *

web.config.debug = True

db = web.database(
    host = 'ricter.info',
    dbn  = 'mysql',
    db   = 'ricter_newanime', 
    user = 'ricter', 
    pw   = ''
)
