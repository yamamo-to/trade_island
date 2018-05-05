# trade_island
GMOクリック証券のトレードアイランドからデータを取得するライブラリです。
ウェブサイトを回覧してランキング情報をpandasのDafaFrame型として取得します。

## 使い方

回覧したウェブサイトを保存するために、予めディレクトリを作成します。
```
mkdir cache
```
サンプルコードは以下の通りです。
```python
import trade_island

cache_dir = 'cache'
trade_island.download_rank_pages(cache_dir)
ranks = trade_island.get_ranks(cache_dir)
df = ranks.to_dataframe()
```
