import csv

with open('top_cities.csv','w',newline='') as f:
  # 第一引数にファイルオブジェクトを、第二引数にフィールド名のリストを指定する
  writer = csv.DictWriter(f,['rank', 'city', 'population'])
  writer.writeheader() # １行目のヘッダーを出力する
  # writerows()で複数の行を一度に出力する、引数は辞書のリスト
  writer.writerows([
    {'rank': 1, 'city': '上海', 'population': 24150000},
    {'rank': 2, 'city': 'カラチ', 'population': 11150000},
    {'rank': 3, 'city': '北京', 'population': 12450000},
    {'rank': 4, 'city': '天津', 'population': 22250000},
    ])
