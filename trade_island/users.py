import pandas as pd
import bs4
from trade_island.util import split_unit


class Users(object):
    """ユーザを格納するクラス"""

    def __init__(self):
        self.users = {}

    def get_user_by_uid(self, uid):
        """
        ユーザIDからユーザ情報を取得する。

        Parameters
        ----------
        uid : str
            ユーザID。

        Returns
        -------
        user : dict
            ユーザ情報。
        """
        return self.users[uid]

    def parse_html(self, html):
        """
        ランキングページ(HTML)からユーザ情報を抽出する。

        Parameters
        ----------
        html : str
            ランキングページ。

        Returns
        -------
        rank_users : list
            ユーザのリスト。
        """
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tr_count = 0
        for tr in soup.tbody.find_all('tr'):
            tag_td = tr.find_all('td')

            if tr_count % 3 == 0:
                user = {}
                class_name = tag_td[0].get('class').pop(0)
                if class_name == 'rank_no':
                    user['順位'] = int(split_unit(tag_td[0].string)[0])

                class_name = tag_td[2].get('class').pop(0)
                if class_name == 'nickname':
                    user['ニックネーム'] = tag_td[2].string
                    href = tag_td[2].a.get('href')
                    user['uid'] = href[href.find('=') + 1:]

                user['収益率'] = float(split_unit(tag_td[3].string)[0])
                user['現在資産'] = int(split_unit(tag_td[4].string)[0])
                user['株式回数'] = int(split_unit(tag_td[5].string)[0])
                user['先OP回数'] = int(split_unit(tag_td[6].string)[0])
                user['FXネオ回数'] = int(split_unit(tag_td[7].string)[0])
                user['外為OP回数'] = int(split_unit(tag_td[8].string)[0])
                user['くりっく365回数'] = int(split_unit(tag_td[9].string)[0])
                user['CFD回数'] = int(split_unit(tag_td[10].string)[0])

            elif tr_count % 3 == 1:
                user['収益額'] = int(split_unit(tag_td[0].string)[0])
                user['当初資産'] = int(split_unit(tag_td[1].string)[0])
                user['株式約定代金'] = int(split_unit(tag_td[2].string)[0])
                user['先OP約定代金'] = int(split_unit(tag_td[3].string)[0])
                user['FXネオ約定代金'] = int(split_unit(tag_td[4].string)[0])
                user['外為OP約定代金'] = int(split_unit(tag_td[5].string)[0])
                user['くりっく365約定代金'] = int(split_unit(tag_td[6].string)[0])
                user['CFD約定代金'] = int(split_unit(tag_td[7].string)[0])

            elif tr_count % 3 == 2:
                self.users[user['uid']] = user

            tr_count += 1

    def to_dataframe(self):
        """
        ユーザリストをpandas DataFrameへと変換する。

        Returns
        -------
        df : pandas.DataFrame
            DataFrame
        """
        df = pd.DataFrame()
        df = df.from_items(self.users.items()).T
        df.drop('uid', axis=1)
        df.index.name = 'uid'
        df = df[['順位', 'ニックネーム', '現在資産', '当初資産', '収益率', '収益額',
                 '株式回数', '株式約定代金',
                 '先OP回数', '先OP約定代金',
                 'FXネオ回数', 'FXネオ約定代金',
                 '外為OP回数', '外為OP約定代金',
                 'くりっく365回数', 'くりっく365約定代金',
                 'CFD回数', 'CFD約定代金']]
        return df.sort_values(by='順位')
