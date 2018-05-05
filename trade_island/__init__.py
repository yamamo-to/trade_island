import urllib.request
from trade_island.users import Users
from trade_island.rank_page import get_rank_page_url
from trade_island.rank_page import get_rank_result_num
from trade_island.rank_page import get_max_pages


def download_rank_pages(dir):
    """
    ランキングページを全て取得する。

    Parameters
    ----------
    dir : str
        キャッシュディレクトリ。
    """
    url = 'https://www.click-sec.com/trade/rank.html'
    filename = '{}/rank.html'.format(dir)
    urllib.request.urlretrieve(url, filename)
    with open(filename, 'r') as f:
        html = f.read()
        result_num = get_rank_result_num(html)
        max_pages = get_max_pages(result_num, 100)
        for i in range(max_pages):
            page_id = i + 1
            url = get_rank_page_url(n=100, page_id=page_id)
            filename = '{}/rank_{:04d}.html'.format(dir, page_id)
            urllib.request.urlretrieve(url, filename)


def get_rank_users(dir):
    """
    取得したランキングページからユーザを取得する。

    Parameters
    ----------
    dir : str
        キャッシュディレクトリ。

    users : list
        Usersインスタンス。
    """
    users = Users()
    filename = '{}/rank.html'.format(dir)
    with open(filename, 'r') as f:
        html = f.read()
        result_num = get_rank_result_num(html)
        max_pages = get_max_pages(result_num, 100)
        for i in range(max_pages):
            page_id = i + 1
            filename = '{}/rank_{:04d}.html'.format(dir, page_id)
            with open(filename, 'r') as user_page:
                users.parse_html(user_page.read())
    return users
