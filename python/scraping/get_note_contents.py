import sys

from selenium import webdriver

def main():
  """
  メインの処理
  """

  driver = webdriver.PhantomJS() #
  driver.set_window_size(800, 600) # 

  navigate(driver) # 
  posts = scrape_posts(driver) # 

  # 
  for post in posts:
    print(post)

def navigate(driver):
  """
  目的のページに遷移する
  """

  print('Navigating...', file=sys.stderr)
  driver.get('https://note.mu/') # 
  assert 'note' in driver.title # 

def scrape_posts(driver):
  """
  文章コンテンツのURL、タイトル、概要を含むdictのリストを取得する
  """

  posts = []

  # 
  for a in driver.find_elements_by_css_selector('a.p-post--basic'):

    # 
    posts.append({
      'url': a.get_attribute('href'),
      'title': a.find_element_by_css_selector('h4').text,
      'description': a.find_element_by_css_selector('.c-post__description').text,
    })

  return posts

if __name__ == '__main__':
  main()
