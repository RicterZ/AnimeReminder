#coding=utf-8
from urllib import urlopen;
from time import sleep;
 
while(True):
    print '**update'
    res = urlopen("http://updateanime.ricter.info/allupdate");
    sleep(3600); 
