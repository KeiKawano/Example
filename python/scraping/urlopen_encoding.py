import sys
from urllib.request import Request, urlopen

req = Request('https://gihyo.jp/dp', headers={'User-Agent': 'Mozilla/5.0'})
f = urlopen(req)
# HTTPヘッダからエンコーディングを取得する（明治されていない場合はutf-8とする）
encoding = f.info().get_content_charset(failobj='utf8')
print('encoding:', encoding, file=sys.stderr) # エンコーディングを標準エラー出力に出力する

text = f.read().decode(encoding) # 得られたエンコーディングを指定して文字列にデコードする
print(text) # デコードしたレスポンスボディを標準出力に出力する


