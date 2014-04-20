#coding: utf-8
from django.test import SimpleTestCase
from back_end.parse_bilibili import *


class ParserTest(SimpleTestCase):
    def test_parse_bilibili(self):
        data = get_bilibili_anime_detail('日常')
        self.assertEqual(data['bilibili_aid'], 782)
        self.assertEqual(data['bilibili_bgmcount'], 26)
        self.assertEqual(data['bilibili_season'], 1)

        data = get_bilibili_anime_detail('中二病也要谈恋爱！')
        self.assertEqual(data['bilibili_aid'], 5691)
        self.assertEqual(data['bilibili_bgmcount'], 12)
        self.assertEqual(data['bilibili_season'], 2)

        data = get_bilibili_anime_detail('中二病也要谈恋爱')
        self.assertEqual(data['bilibili_aid'], 5691)
        self.assertEqual(data['bilibili_bgmcount'], 12)
        self.assertEqual(data['bilibili_season'], 2)

        data = get_bilibili_anime_detail('魔法少女小圆')
        self.assertEqual(data['bilibili_bgmcount'], 12)