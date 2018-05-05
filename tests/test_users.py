import unittest
from trade_island.users import Users


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.users = Users()

    def test_parse_html(self):
        with open('tests/rank_test.html', 'r') as f:
            html = f.read()
            self.users.parse_html(html)
            uid = '01234567890123456789012345678901'
            user = self.users.get_user_by_uid(uid)
            self.assertEqual(uid, user['uid'])
            self.assertEqual('テストユーザ1', user['ニックネーム'])
            self.assertEqual(1, user['順位'])

            self.assertEqual(123.4, user['収益率'])
            self.assertEqual(123456, user['現在資産'])
            self.assertEqual(10, user['株式回数'])
            self.assertEqual(20, user['先OP回数'])
            self.assertEqual(30, user['FXネオ回数'])
            self.assertEqual(40, user['外為OP回数'])
            self.assertEqual(50, user['くりっく365回数'])
            self.assertEqual(60, user['CFD回数'])

            self.assertEqual(789012, user['収益額'])
            self.assertEqual(98765, user['当初資産'])
            self.assertEqual(15, user['株式約定代金'])
            self.assertEqual(25, user['先OP約定代金'])
            self.assertEqual(35, user['FXネオ約定代金'])
            self.assertEqual(45, user['外為OP約定代金'])
            self.assertEqual(55, user['くりっく365約定代金'])
            self.assertEqual(65, user['CFD約定代金'])


if __name__ == '__main__':
    unittest.main()
