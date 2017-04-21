import os

from apiclient.discovery import build # pip install google-api-python-client

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY'] # 環境変数からAPIキーを取得

# YouTubeのAPIクライアントを組み立てる。build()関数の第一引数にはAPI名を、第二引数にはAPIのバージョンを指定し、キーワード引数develiperKeyでAPIキーを指定する
# この関数は内部的に「https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest」というURLにアクセスし、APIのリソやメソッドの情報を取得する
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# キーワード引数で引数を指定し、search.listメソッドを呼び出す
# list()メソッドでgoogleapiclient.http.HttptRequestオブジェクトが得られ、execute()メソッドを実行すると実際にHTTPリクエストが送られてAPIのレスポンスが得られる
search_response = youtube.search().list(
    part='snippet',
    q='スターウォーズ',
    type='video',
  ).execute()

# search_responseはAPIのレスポンスのJSONをパーズしたdict
for item in search_response['items']:
  print(item['snippet']['title']) # 動画のタイトルを表示する

