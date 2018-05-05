import urllib.request
from trade_island.ranks import Ranks


def download_rank_pages(dir):
    """
    ランキングページを全て取得する。

    Parameters
    ----------
    dir : str
        キャッシュディレクトリ。
    """
    ranks = Ranks()
    url = 'https://www.click-sec.com/trade/rank.html'
    filename = '{}/rank.html'.format(dir)
    urllib.request.urlretrieve(url, filename)
    with open(filename, 'r') as f:
        html = f.read()
        result_num = ranks.get_rank_result_num(html)
        max_pages = ranks.get_max_pages(result_num, 100)
        for i in range(max_pages):
            page_id = i + 1
            url = ranks.get_rank_page_url(n=100, page_id=page_id)
            filename = '{}/rank_{:04d}.html'.format(dir, page_id)
            urllib.request.urlretrieve(url, filename)


def get_ranks(dir):
    """
    取得したランキングページからユーザを取得する。

    Parameters
    ----------
    dir : str
        キャッシュディレクトリ。

    ranks : list
        Ranksインスタンス。
    """
    ranks = Ranks()
    filename = '{}/rank.html'.format(dir)
    with open(filename, 'r') as f:
        html = f.read()
        result_num = ranks.get_rank_result_num(html)
        max_pages = ranks.get_max_pages(result_num, 100)
        for i in range(max_pages):
            page_id = i + 1
            filename = '{}/rank_{:04d}.html'.format(dir, page_id)
            with open(filename, 'r') as page:
                ranks.parse_html(page.read())
    return ranks
