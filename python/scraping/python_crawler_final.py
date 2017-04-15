import time
import re

import requests
import lxml.html
from pymongo import MongoClient

def main():
  """
  クローラーのメインの処理
  """
  client = MongoClient('localhost', 27017) # ローカルホストのMongoDBに接続する
  collection = client.scraping.ebooks # scrapingデータベースのebooksコレクションを得る
  # データを一意に識別するキーを格納するkeyフィールドにユニークなインデックスを作成する
  collection.create_index('key', unique=True)
  session = requests.Session() # 複数のページをスクロールするのでSessionを使う
  response = session.get('https://gihyo.jp/dp') # 一覧ページを取得する
  urls = scrape_list_page(response) # 詳細ページのURL一覧を得る
  for url in urls: # ジェネレーターイテレーターはlistなどと同様に繰り返し可能
    key = extract_key(url) # URLからキーを取得する
    ebook = collection.find_one({'key': key}) # MongoDBからkeyに該当するデータを探す
    if not ebook: # MongoDBに存在しない場合だけ、詳細ページをスクロールする
      time.sleep(1) # 1秒のウェイトを入れる
      response = requests.get(url)
      ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る
      print(ebook)
      collection.insert_one(ebook) # 電子書籍の情報をMongoDBに保存する
    
    print(ebook) # 電子書籍の情報を表示

def scrape_list_page(response):
  """
  一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数
  """
  root = lxml.html.fromstring(response.content)
  root.make_links_absolute(response.url)

  for a in root.cssselect('#listBook a[itemprop="url"]'):
    url = a.get('href')
    yield url

def scrape_detail_page(response):
  """
  詳細ページのResponseから電子書籍の情報をdectで取得する
  """
  root = lxml.html.fromstring(response.content)
  ebook = {
    'url': response.url, # URL
    'key': extract_key(response.url), # URLから抜き出したキー
    'title': root.cssselect('#bookTitle')[0].text_content(), # タイトル
    'price': root.cssselect('.buy')[0].text.strip(), # 価格（.textで直接の子である文字列のみを取得）
    'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')], # 目次
  }
  return ebook # dictを返す

def extract_key(url):
  """
  URLからキー（URLの末尾のISBN）を抜き出す
  """
  m = re.search(r'/([^/]+)$', url)
  return m.group(1)
  
  
def normalize_spaces(s):
  """
  連続する空白を１つのスペースに置き換える
  前後の空白は削除した新しい文字列を取得する
  """
  return re.sub(r'\s+', '', s).strip()

if __name__ == '__main__':
  main()