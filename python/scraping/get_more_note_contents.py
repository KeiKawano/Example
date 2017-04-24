import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def main():
  """
  メインの処理
  """

  driver = webdriver.PhantomJS() #
  driver.set_window_size(800, 600) # 

  navigate(driver) # 
  posts = scrape_posts(driver) # 

  # コンテンツの情報を表示する
  for post in posts:
    print(post)

def navigate(driver):
  """
  目的のページに遷移して続きのコンテンツを読み込む
  """

  print('Navigating...', file=sys.stderr)
  driver.get('https://note.mu/') # 
  assert 'note' in driver.title # 

  # ページの１番下までスクロールする
  driver.execute_script('scroll(0, document.body.scrollHeight)')

  print('Waiting for contents to be loaded...', file=sys.stderr)
  time.sleep(2) # ２秒まつ

  # ページの１番下までスクロールする
  driver.execute_script('scroll(0, document.body.scrollHeight)')

  # 10秒でタイムアウトするWebDriverWaitオブジェクトを作成する
  wait = WebDriverWait(driver, 15)

  print('Waitint for the more button to be clickable...', file=sys.stderr)
  # 「もっとみる」ボタンがクリック可能になるまで待つ
  button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-more')))

  button.click() # 「もっとみる」ボタンをクリックする

  print('Waiting for contents to be loaded...', file=sys.stderr)
  time.sleep(2) # 2秒待つ

def scrape_posts(driver):
  """
  文章コンテンツのURL、タイトル、概要を含むdictのリストを取得する
  """

  posts = []

  # すべての文章コンテンツを表すa要素について反復する
  for a in driver.find_elements_by_css_selector('a.p-post--basic'):

    # URL、タイトル、概要を取得して、dictとしてリストに追加する
    posts.append({
      'url': a.get_attribute('href'),
      'title': a.find_element_by_css_selector('h4').text,
      'description': a.find_element_by_css_selector('.c-post__description').text,
    })

  return posts

if __name__ == '__main__':
  main()
