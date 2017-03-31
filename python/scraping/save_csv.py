import csv

# ファイルを書き込みように開く。newline=''とすることで改行コードの自動変換を制御する
with open('top_cities.csv','w',newline='') as f:
  writer = csv.writer(f) # writer()は引数にファイルオブジェクトを指定する
  writer.writerow(['rank', 'city', 'population']) # １行目のヘッダを出力する
  # writerows()で複数の行を一度に出力する。引数はリストのリスト
  writer.writerows([
    [1, '上海', 2415000],
    [2, 'カラチ', 2315000],
    [3, '天津', 2415000]
    ])