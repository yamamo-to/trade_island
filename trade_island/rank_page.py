import urllib.request
import urllib.parse
import bs4
import math
from collections import OrderedDict


def get_rank_page_url(n=None, page_id=None):
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


def get_rank_result_num(html):
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


def get_max_pages(result_num, n):
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
