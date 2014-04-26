#coding: utf-8
from django.test import SimpleTestCase
from back_end.parse_bilibili import *
from back_end.parse_kankan import *


class ParserTest(SimpleTestCase):
    def test_parse_bilibili(self):
        data = get_bilibili_anime_detail('日常')
        self.assertEqual(data['bilibili_aid'], 782)
        self.assertEqual(data['bilibili_bgmcount'], 28)
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
        self.assertEqual(data['bilibili_bgmcount'], 13)

        data = get_bilibili_anime_detail('幸运星')
        print data
        self.assertEqual(data['bilibili_bgmcount'], 24)

    def test_search_anime(self):
        data = search_anime('魔法少女小圆')
        print data
        self.assertEqual([('魔法少女小圆', '60075'), ('魔法少女小圆 剧场版', '73391')], data)