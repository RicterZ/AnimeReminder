#coding: utf-8
import unittest
from bilibili import get_anime_detail


class ParserTest(unittest.TestCase):
    def test_parse_bilibili(self):

        data = get_anime_detail('疑犯追踪')
        self.assertEqual(data['aid'], 17309)
        self.assertEqual(data['episode'], 61)

        data = get_anime_detail('日常')
        self.assertEqual(data['aid'], 782)
        self.assertEqual(data['episode'], 28)

        data = get_anime_detail('中二病也要谈恋爱！')
        self.assertEqual(data['aid'], 5691)
        self.assertEqual(data['episode'], 22)

        data = get_anime_detail('中二病也要谈恋爱')
        self.assertEqual(data['aid'], 5691)
        self.assertEqual(data['episode'], 22)

        data = get_anime_detail('魔法少女小圆')
        self.assertEqual(data['episode'], 1)

        data = get_anime_detail('幸运星')
        self.assertEqual(data['episode'], 2)

    '''
    def test_search_anime(self):
        data = search_anime('魔法少女小圆')
        print data

        data = search_anime('日常')
        print data

        data = search_anime('qwidfdsigwngfkivj')
        print data
    '''


if __name__ == '__main__':
    unittest.main()