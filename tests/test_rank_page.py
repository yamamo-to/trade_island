import unittest
from trade_island.rank_page import get_rank_page_url
from trade_island.rank_page import get_rank_result_num
from trade_island.rank_page import get_max_pages


class TestRankPages(unittest.TestCase):

    def test_get_rank_page_url(self):
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html',
            get_rank_page_url())
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html?n=100',
            get_rank_page_url(100))
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html?n=100&pageID=3',
            get_rank_page_url(100, 3))
        self.assertEqual(
            'https://www.click-sec.com/trade/rank.html?pageID=2',
            get_rank_page_url(page_id=2))

    def test_get_rank_result_num(self):
        with open('tests/rank_test.html', 'r') as f:
            html = f.read()
            self.assertEqual(18157, get_rank_result_num(html))

    def test_get_max_pages(self):
        self.assertEqual(0, get_max_pages(0, 100))
        self.assertEqual(1, get_max_pages(1, 100))
        self.assertEqual(1, get_max_pages(99, 100))
        self.assertEqual(1, get_max_pages(100, 100))
        self.assertEqual(2, get_max_pages(101, 100))


if __name__ == '__main__':
    unittest.main()
