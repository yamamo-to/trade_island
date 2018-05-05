import math
import urllib.request
import bs4
import pandas as pd
from collections import OrderedDict
from trade_island.util import split_unit


class Ranks(object):
    """ユーザランキング情報を格納するクラス"""

    def __init__(self):
        self.ranks = {}

    def get_rank_by_uid(self, uid):
        """
        ユーザIDからユーザのランキング情報を取得する。

        Parameters
        ----------
        uid : str
            ユーザID。

        Returns
        -------
        rank : dict
            ユーザランキング情報。
        """
        return self.ranks[uid]

    def parse_html(self, html):
        """
        ランキングページ(HTML)からユーザランキング情報を抽出する。

        Parameters
        ----------
        html : str
            ランキングページ。

        Returns
        -------
        rank_ranks : list
            ユーザランキング情報のリスト。
        """
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tr_count = 0
        for tr in soup.tbody.find_all('tr'):
            tag_td = tr.find_all('td')

            if tr_count % 3 == 0:
                rank = {}
                class_name = tag_td[0].get('class').pop(0)
                if class_name == 'rank_no':
                    rank['順位'] = int(split_unit(tag_td[0].string)[0])

                class_name = tag_td[2].get('class').pop(0)
                if class_name == 'nickname':
                    rank['ニックネーム'] = tag_td[2].string
                    href = tag_td[2].a.get('href')
                    rank['uid'] = href[href.find('=') + 1:]

                rank['収益率'] = float(split_unit(tag_td[3].string)[0])
                rank['現在資産'] = int(split_unit(tag_td[4].string)[0])
                rank['株式回数'] = int(split_unit(tag_td[5].string)[0])
                rank['先OP回数'] = int(split_unit(tag_td[6].string)[0])
                rank['FXネオ回数'] = int(split_unit(tag_td[7].string)[0])
                rank['外為OP回数'] = int(split_unit(tag_td[8].string)[0])
                rank['くりっく365回数'] = int(split_unit(tag_td[9].string)[0])
                rank['CFD回数'] = int(split_unit(tag_td[10].string)[0])

            elif tr_count % 3 == 1:
                rank['収益額'] = int(split_unit(tag_td[0].string)[0])
                rank['当初資産'] = int(split_unit(tag_td[1].string)[0])
                rank['株式約定代金'] = int(split_unit(tag_td[2].string)[0])
                rank['先OP約定代金'] = int(split_unit(tag_td[3].string)[0])
                rank['FXネオ約定代金'] = int(split_unit(tag_td[4].string)[0])
                rank['外為OP約定代金'] = int(split_unit(tag_td[5].string)[0])
                rank['くりっく365約定代金'] = int(split_unit(tag_td[6].string)[0])
                rank['CFD約定代金'] = int(split_unit(tag_td[7].string)[0])

            elif tr_count % 3 == 2:
                self.ranks[rank['uid']] = rank

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
        df = df.from_items(self.ranks.items()).T
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

    def get_rank_page_url(self, n=None, page_id=None):
        """
        ランキングページのURLを作成する。

        Parameters
        ----------
        n : int
            ページあたりの表示件数を指定する。20以上100以下の数値。
        page_id :
            ページ番号。

        Returns
        -------
        rank_page_url : str
            ランキングページのURL。
        """
        d = OrderedDict()
        if n is not None:
            d['n'] = n
        if page_id is not None:
            d['pageID'] = page_id
        param = urllib.parse.urlencode(d, True)
        url = 'https://www.click-sec.com/trade/rank.html'
        if len(param) > 0:
            url += '?{}'.format(param)
        return url

    def get_rank_result_num(self, html):
        """
        ランキングページ(HTML)から総ページ数を抽出する。

        Parameters
        ----------
        html : str
            ランキングページのHTML。

        Returns
        -------
        rank_result_num : int
            ランキングページの総ページ数。
        """
        soup = bs4.BeautifulSoup(html, 'html.parser')
        span = soup.find_all('span')
        rank_result_num = 0
        for tag in span:
            try:
                s = tag.get("class").pop(0)
                if s in "rank_result_num":
                    rank_result_num = int(tag.string.replace(',', ''))
                    break
            except:
                pass
        return rank_result_num

    def get_max_pages(self, result_num, n):
        """
        参加者数とページあたりの表示ユーザ数から最大のページ数を求める。

        Parameters
        ----------
        result_num : int
            参加者数。
        n : int
            ページあたりの表示ユーザ数。

        Returns
        -------
        max_pages : int
            最大のページ数。
        """
        return math.floor((result_num - 1) / n) + 1
