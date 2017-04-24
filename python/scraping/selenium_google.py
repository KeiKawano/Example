from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# PhantomJSのWebDriverオブジェクトを作成する
driver = webdriver.PhantomJS()

# Googleのトップ画面を開く
driver.get('https://www.google.co.jp/')

# タイトルにGoogleが含まれていることを確認する
assert 'Google' in driver.title

# 検索キーワードの準備
search_word = 'StarWars'
# 検索語を入力して送信する
input_element = driver.find_element_by_name('q')
input_element.send_keys(search_word)
input_element.send_keys(Keys.RETURN)

# タイトルに「StarWars」が含まれていることを確認する
assert search_word in driver.title

# スクリーンショットを撮る
driver.save_screenshot('search_results.png')

# 検索結果を表示する
for a in driver.find_elements_by_css_selector('h3 > a'):
  print(a.text)
  print(a.get_attribute('href'))
