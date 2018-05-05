import unittest
from trade_island.ranks import Ranks


class TestRanks(unittest.TestCase):

    def setUp(self):
        self.ranks = Ranks()

    def test_parse_html(self):
        with open('tests/rank_test.html', 'r') as f:
            html = f.read()
            self.ranks.parse_html(html)
            uid = '01234567890123456789012345678901'
            rank = self.ranks.get_rank_by_uid(uid)
            self.assertEqual(uid, rank['uid'])
            self.assertEqual('テストユーザ1', rank['ニックネーム'])
            self.assertEqual(1, rank['順位'])

            self.assertEqual(123.4, rank['収益率'])
            self.assertEqual(123456, rank['現在資産'])
            self.assertEqual(10, rank['株式回数'])
            self.assertEqual(20, rank['先OP回数'])
            self.assertEqual(30, rank['FXネオ回数'])
            self.assertEqual(40, rank['外為OP回数'])
            self.assertEqual(50, rank['くりっく365回数'])
            self.assertEqual(60, rank['CFD回数'])

            self.assertEqual(789012, rank['収益額'])
            self.assertEqual(98765, rank['当初資産'])
            self.assertEqual(15, rank['株式約定代金'])
            self.assertEqual(25, rank['先OP約定代金'])
            self.assertEqual(35, rank['FXネオ約定代金'])
            self.assertEqual(45, rank['外為OP約定代金'])
            self.assertEqual(55, rank['くりっく365約定代金'])
            self.assertEqual(65, rank['CFD約定代金'])

    def test_get_rank_page_url(self):
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html',
            self.ranks.get_rank_page_url())
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html?n=100',
            self.ranks.get_rank_page_url(100))
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html?n=100&pageID=3',
            self.ranks.get_rank_page_url(100, 3))
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html?pageID=2',
            self.ranks.get_rank_page_url(page_id=2))

    def test_get_rank_result_num(self):
        with open('tests/rank_test.html', 'r') as f:
            html = f.read()
            self.assertEqual(18157, self.ranks.get_rank_result_num(html))

    def test_get_max_pages(self):
        self.assertEqual(0, self.ranks.get_max_pages(0, 100))
        self.assertEqual(1, self.ranks.get_max_pages(1, 100))
        self.assertEqual(1, self.ranks.get_max_pages(99, 100))
        self.assertEqual(1, self.ranks.get_max_pages(100, 100))
        self.assertEqual(2, self.ranks.get_max_pages(101, 100))


if __name__ == '__main__':
    unittest.main()
