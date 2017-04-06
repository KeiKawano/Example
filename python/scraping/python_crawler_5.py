import re
import requests
import lxml.html

def main():
  """
  クローラーのメインの処理
  """
  session = requests.Session() # 複数のページをスクロールするのでSessionを使う
  response = session.get('https://gihyo.jp/dp')
  urls = scrape_list_page(response)
  for url in urls: # ジェネレーターイテレーターはlistなどと同様に繰り返し可能
    response = session.get(url) # Sessionを使って詳細ページを取得する
    ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る
    print(ebook)
    break # まず１ページだけで試すため、break文でループを抜ける

def scrape_list_page(response):
  """
  一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数
  """
  root = lxml.html.fromstring(response.content)
  root.make_links_absolute(response.url)

  for a in root.cssselect('#listBook a[itemprop="url"]'):
    url = a.get('href')
    yield url # 

def scrape_detail_page(response):
  """
  詳細ページのResponseから電子書籍の情報をdectで取得する
  """
  root = lxml.html.fromstring(response.content)
  ebook = {
    'url': response.url, # URL
    'title': root.cssselect('#bookTitle')[0].text_content(), # タイトル
    'price': root.cssselect('.buy')[0].text.strip(), # 価格（.textで直接の子である文字列のみを取得）
    'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')], # 目次
  }
  return ebook # dictを返す
  
def normalize_spaces(s):
  """
  連続する空白を１つのスペースに置き換える
  前後の空白は削除した新しい文字列を取得する
  """
  return re.sub(r'\s+', '', s).strip()

if __name__ == '__main__':
  main()