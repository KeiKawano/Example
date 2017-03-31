import json

cities = [
  {'rank': 1, 'city': '上海', 'population': 24150000},
  {'rank': 2, 'city': 'カラチ', 'population': 11150000},
  {'rank': 3, 'city': '北京', 'population': 12450000},
  {'rank': 4, 'city': '天津', 'population': 22250000},
]

print(json.dumps(cities, ensure_ascii=False, indent=2))