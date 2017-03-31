import sqlite3

conn = sqlite3.connect('top_cities.db') # 

c = conn.cursor() # 
# 
# 
c.execute('DROP TABLE IF EXISTS cities')
# 
c.execute('''
  CREATE TABLE cities (
    rank integer,
    city text,
    population integer
  )
  ''')

# 
# 
c.execute('INSERT INTO cities VALUES (?,?,?)',(1, '上海', 2415000))

# 
c.execute('INSERT INTO cities VALUES (:rank,:city,:population)',{'rank':2, 'city':'カラチ', 'population':1111000})

# 
# 
c.executemany('INSERT INTO cities VALUES (:rank,:city,:population)', [
    {'rank': 3, 'city': '北京', 'population':3333000},
    {'rank': 4, 'city': '天津', 'population':4444000},
    {'rank': 5, 'city': 'イスタンブル', 'population':555000},
    {'rank': 6, 'city': 'ホーチミン', 'population':6666000},
    {'rank': 7, 'city': 'プノンペン', 'population':7777000},
  ])

conn.commit() # 

c.execute('SELECT * FROM cities') # 

for row in c.fetchall():
  print(row) # 

conn.close() # 

