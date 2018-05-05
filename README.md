# trade_island
GMOクリック証券のトレードアイランドからデータを取得するライブラリです。
ウェブサイトを回覧してランキング情報を得ます。

## 使い方

```python
import trade_island

cache_dir = 'cache'
trade_island.download_rank_pages(cache_dir)
users = trade_island.get_rank_users(cache_dir)
df = users.to_dataframe()
```
