#coding: utf-8
from django.test import TestCase
from back_end.parse_bilibili import *


class ParserTest(TestCase):
    def test_parse_bilibili(self):
        data = get_bilibili_anime_detail('日常')
        self.assertEqual(data['bilibili_aid'], "782")
        self.assertEqual(data['bilibili_bgmcount'], 26)
        self.assertEqual(data['bilibili_season'], 1)