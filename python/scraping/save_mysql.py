import MySQLdb

# MySQLサーバーに接続し、コネクションを取得する
# ユーザー名とパスワードを指定してscrapingデータベースを使用する。接続に使用する文字コードはutf8mb4とする
conn = MySQLdb.connect(db='scraping', user='scraper', passwd='password', charset='utf8mb4')

c = conn.cursor() # カーソルを取得する
# execute()メソッドでSQL文を実行する
# このスクリプトを何回実行しても同じ結果になるようにするため、citiesテーブルが存在する場合は削除する
c.execute('DROP TABLE IF EXISTS cities')
# citiesテーブルを作成する
c.execute('''
  CREATE TABLE cities (
    rank integer,
    city text,
    population integer
  )
''')

# execute()メソッドの第２引数にはSQL文のパラメータを指定できる
# パラメータで置き換える場所（プレースホルダー）は％ｓで指定する
c.execute('INSERT INTO cities VALUES (%s, %s, %s)', (1, '上海', 24150000))

# パラメータが辞書の場合、プレースホルダは％（名前）sで指定する
c.execute('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)', {'rank': 2, 
'city': 'カラチ', 'population': 23500000})

# execcutemany()メソッドは、複数のパラメータをリストで指定し、複数（ここでは３つ）のSQL文を実行する
c.executemany('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)', [
  {'rank': 3, 'city': '北京', 'population': 21516000},
  {'rank': 4, 'city': '天津', 'population': 14722100},
  {'rank': 5, 'city': 'イスタンブル', 'population': 14160467}
])

conn.commit() # 変更をコミットする

c.execute('SELECT * FROM cities') # 保存したデータを取得する
for row in c.fetchall(): # クエリの結果はfetchall()メソどdで取得できる
  print(row) # 取得したデータを表示する

conn.close() # コネクションをクローズする
  