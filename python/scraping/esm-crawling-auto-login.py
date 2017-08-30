import sys
import os
import time

from robobrowser import RoboBrowser

# 認証の情報は環境変数から取得する。
ESM_ID = os.environ['ESM_ID']
ESM_PASS = os.environ['ESM_PASS']

# RoboBrowserオブジェクトを作成する。
browser = RoboBrowser(
    parser='html.parser',  # Beautiful Soupで使用するパーサーを指定する。
    # Cookieが使用できないと表示されてログインできない問題を回避するため、通常のブラウザーのUser-Agent（ここではFirefoxのもの）を使う。
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0')


def main():
    # トップページを開く。
    print('Navigating...', file=sys.stderr)
    browser.open('https://mkweb.sint.co.jp/esm/esales-pc')

    # タイトルが「eセールスマネージャーRemix」になっていることを確認する。
    assert 'eセールスマネージャーRemix' in browser.parsed.title.string

    # name="myform2" というサインインフォームを埋める。
    # フォームのname属性の値はブラウザーの開発者ツールで確認できる。
    form = browser.get_form(attrs={'name': 'myform2'})
    form['id'] = ESM_ID  # name="id" という入力ボックスを埋める。
    form['password'] = ESM_PASS  # name="id" という入力ボックスを埋める。

    # フォームを送信する。正常にログインするにはRefererヘッダーとAccept-Languageヘッダーが必要。
    print('Signing in...', file=sys.stderr)
    browser.submit_form(form, headers={
        'Referer': browser.url,
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
    })

    # ログインに失敗する場合は、次の行のコメントを外してHTMLのソースを確認すると良い。
    print(browser.parsed.prettify())

    assert 'eセールスマネージャーRemix' in browser.parsed.title.string

    print('get iframe')
    # iframeの要素を取得する
    iframe_element = browser.select('#mainframe')
    print(iframe_element)
    iframe_src = iframe_element.select_one('')


    print('go to print_order_history')



    print_order_history()  # 注文履歴を表示する。

    # link_to_next = browser.get_link('次へ')  # 「次へ」というテキストを持つリンクを取得する。
    # if not link_to_next:
    #     break  # 「次へ」のリンクがない場合はループを抜けて終了する。

    # print('Following link to next page...', file=sys.stderr)
    # browser.follow_link(link_to_next)  # 「次へ」というリンクをたどる。
    print('..end')


def print_order_history():
    """
    今日のスケジュールを取得する
    """
    # ページ内の今日のスケジュールについて反復する。ブラウザーの開発者ツールでclass属性の値を確認できる。
    for line_item in browser.select('.schedule_today'):
        schedule_today = {}  # スケジュールの情報を格納するためのdict。
        # スケジュールの情報のすべての列について反復する。
        for column in line_item.select('.schedule_content'):
            time_element = column.select_one('.schedule_time_default')
            title_element = column.select_one('.sch_title')
            # 時間とタイトルがない列は無視する。
            if time_element and title_element:
                time = time_element.get_text().strip()
                title = title_element.get_text().strip()
                schedule_today['時間'] = time  # スケジュールの情報を格納する。
                schedule_today['タイトル'] = title  # スケジュールの情報を格納する。

        print(schedule_today['時間'], schedule_today['タイトル'])  # スケジュールの情報を表示する。

if __name__ == '__main__':
    main()
