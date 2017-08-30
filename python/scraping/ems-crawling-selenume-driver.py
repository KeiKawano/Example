import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 認証の情報は環境変数から取得する。
ESM_ID = os.environ['ESM_ID']
ESM_PASS = os.environ['ESM_PASS']

# PhantomJSのWebDriverオブジェクトを作成する。
driver = webdriver.PhantomJS()

# Googleのトップ画面を開く。
driver.get('https://mkweb.sint.co.jp/esm/esales-pc')

# タイトルに'Google'が含まれていることを確認する。
print(driver.title)
assert 'eセールスマネージャーRemix' in driver.title

# 検索語を入力して送信する。
input_element = driver.find_element_by_name('myform2')
login_id = input_element.find_element_by_name('id')
password = input_element.find_element_by_name('password')
login_id.send_keys(ESM_ID)
password.send_keys(ESM_PASS)
# input_element.send_keys(Keys.RETURN)
password.submit()

time.sleep(5)

# タイトルに'Python'が含まれていることを確認する。
assert 'eセールスマネージャーRemix' in driver.title

# スクリーンショットを撮る。
driver.save_screenshot('esm_results.png')
# html = driver.page_source.encode('utf-8')
html = driver.page_source
driver.quit()
print('driver quit')
print(html)


# 検索結果を表示する。
# for a in driver.find_elements_by_css_selector('h3 > a'):
#     print(a.text)
#     print(a.get_attribute('href'))