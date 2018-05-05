import re


def split_unit(string):
    """
    単位付きの数値文字列を数値と単位に分離する

    Parameters
    ----------
    string : str
        単位付き数値文字列

    Returns
    -------
    value : string
        数値文字列
    unit : str
        単位
    """
    numeric = '''
        (
            [-+]? # 符号
            \d+ # 整数部
            (?: \.\d*)? # 小数部
        )
        \s* # 空白文字
        (
            .* # 任意の文字列
        )
        '''
    pattern = re.compile(numeric, re.VERBOSE)
    s = string.replace(',', '')
    m = pattern.match(s)
    return m.group(1), m.group(2)
