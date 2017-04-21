import os
import sys

from apiclient.discovery import build
from pymongo import MongoClient, DESCENDING

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY'] # 環境変数からAPIキーを取得

def main():
  """
  メインの処理
  """
  mongo_client = MongoClient('localhost', 27017) # MongoDBのクライアントオブジェクトを作成する
  collection = mongo_client.youtube.videos # youtubeデータベースのvideosコレクションを取得
  collection.delete_many({}) # 既存のすべてのドキュメントを削除しておく

  # 
  for items_per_page in search_videos('スターウォーズ'):
    save_to_mongodb(collection, items_per_page)

  # show_top_videos(collection) # ビュー数の多い動画を表示する

def search_videos(query, max_pages=5):
  """
  動画を検索してページ単位でlistをyieldする
  """
  youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY) # YouTubeのクライアントを組み立てる

  # 
  search_request = youtube.search().list(
    part='id', # search.listでは動画IDだけを取得できればOK
    q=query,
    type='video',
    maxResult=50, # 1ページあたり最大50件の動画を取得する
  )

  # リクエストが有効、かつページ数がmax_pages以内の間、繰り返す
  # ページ数を制限しているのは実行時間が長くなり過ぎないようにするためなので、実際にはもっと多くのページを取得してもよい
  i = 0
  while search_request and i < max_pages:
    search_response = search_request.execute() # リクエストを送信
    video_ids = [item['id']['videoId'] for item in search_response['items']] # 動画IDのリストを得る
    # videos.listメソッドで動画の詳細な情報を得る
    videos_response = youtube.videos().list(
      part='snippet,statistics',
      id=','.join(video_ids)
    ).execute()

    yield videos_response['items'] # ページに対応するitemsをyieldする

    # 
    search_request = youtube.search().list_next(search_request, search_response)
    i += 1

def save_to_mongodb(collection, items):
  """
  MongoDBにアイテムのリストを保存する
  """
  # MongoDBに書き換える前に使いやすいようにアイテムを書き換える
  for item in items:
    item['_id'] = item['id'] # 各アイテムのid属性を_id属性として使う

  # statisticsに含まれるviewCountプロパティなどの値が文字列になっいるので数値に変換する
  for key, value in item['statistics'].items():
    item['statistics']['key'] = int(value)

  result = collection.insert_many(items) # コレクションに挿入する
  print('Inserted {0} documents'.format(len(result.inserted_ids)), file=sys.stderr)

def show_top_videos(collecton):
  """
  MongoDBのコレクション内でビュー数の上位5件を表示する
  """
  for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
    print(item['statistics']['viewCount'], item['snippet']['title'])


if __name__ == '__main__':
  main()

