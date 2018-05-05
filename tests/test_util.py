import unittest
from trade_island.util import split_unit


class TestUtil(unittest.TestCase):

    def test_split_unit(self):
        value, unit = split_unit('123 回')
        self.assertEqual('123', value)
        self.assertEqual('回', unit)

        value, unit = split_unit('18,104 位')
        self.assertEqual('18104', value)
        self.assertEqual('位', unit)

        value, unit = split_unit('300 千円')
        self.assertEqual('300', value)
        self.assertEqual('千円', unit)

        value, unit = split_unit('173,971,549円')
        self.assertEqual('173971549', value)
        self.assertEqual('円', unit)

        value, unit = split_unit('+14.4 ％')
        self.assertEqual('+14.4', value)
        self.assertEqual('％', unit)

        value, unit = split_unit('-11.6 ％')
        self.assertEqual('-11.6', value)
        self.assertEqual('％', unit)

        value, unit = split_unit('-15,178,410 円')
        self.assertEqual('-15178410', value)
        self.assertEqual('円', unit)


if __name__ == '__main__':
    unittest.main()
