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
#web.header('Content-type', "text/html; charset=utf-8")

db = web.database(
    host = 'ricter.info',
    dbn  = 'mysql',
    db   = 'ricter_newanime', 
    user = 'ricter', 
    pw   = 'CanyueROOTSmile'
)
