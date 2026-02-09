import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID    = os.environ["USER_ID"]

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"
COUNT_FILE = "last_count.txt"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages":[{"type":"text","text": message}]
    }
    requests.post(url, headers=headers, json=data)

# ページ取得
res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")
page_text = soup.get_text()

# 「在庫なし」の数を数える
current_count = page_text.count("在庫なし")

# 前回の数を読む
try:
    with open(COUNT_FILE, "r", encoding="utf-8") as f:
        last_count = int(f.read().strip())
except:
    last_count = None

# 数が増えたら通知
if last_count is not None and current_count > last_count:
    send_line_message(
        f"在庫状況が変わりました\n在庫なしの表示数：{last_count} → {current_count}"
    )
    print("通知送信")

# 今回の数を保存
with open(COUNT_FILE, "w", encoding="utf-8") as f:
    f.write(str(current_count))
