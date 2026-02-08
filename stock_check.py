import requests
from bs4 import BeautifulSoup
import os

# GitHubのSecretsから取得
LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID    = os.environ["USER_ID"]

# 在庫確認URL
URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

# 前回の在庫状況を保存するファイル
STATUS_FILE = "last_status.txt"

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
page_text = soup.get_text().replace("\n","").replace(" ","")

# 在庫判定
if "在庫なし" in page_text:
    current_status = "在庫なし"
else:
    current_status = "在庫あり"

# 前回の状態を読み込む
try:
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        last_status = f.read().strip()
except FileNotFoundError:
    last_status = None  # 初回はファイルがない

# 状態が変わった場合のみ通知
if current_status != last_status:
    send_line_message(f"在庫状況が変わりました")  # ←通知文
    print(f"通知送信: {current_status}")

# 現在の状態を保存
with open(STATUS_FILE, "w", encoding="utf-8") as f:
    f.write(current_status)

