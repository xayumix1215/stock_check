import requests
from bs4 import BeautifulSoup
import os

# LINE情報（GitHub Secrets から取得）
LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

# チェックするURL
URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

LAST_COUNT_FILE = "last_count.txt"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, json=data)

def get_last_count():
    if os.path.exists(LAST_COUNT_FILE):
        with open(LAST_COUNT_FILE, "r") as f:
            return int(f.read().strip())
    return None

def save_last_count(count):
    with open(LAST_COUNT_FILE, "w") as f:
        f.write(str(count))

def check_stock():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    page_text = soup.get_text()
    current_count = page_text.count("在庫なし")

    last_count = get_last_count()

    # 初回実行時は保存だけ（通知しない）
    if last_count is None:
        save_last_count(current_count)
        print(f"初回記録: 在庫なし {current_count}件")
        return

    # 個数が変わったら通知
    if current_count != last_count:
        send_line_message("在庫状況が変わりました")
        print(f"変化あり: {last_count} → {current_count}")
        save_last_count(current_count)
    else:
        print("変化なし")

check_stock()
